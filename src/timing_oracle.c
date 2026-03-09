/*
 * MEGALODON Project 1 — Timing Oracle on CRYSTALS-Kyber
 * =====================================================
 * Measures decapsulation timing variations in the Kyber
 * reference implementation to detect side-channel leakage.
 *
 * Target: Kyber-512 (NIST PQC Round 3 reference)
 * Method: Crafted ciphertexts → high-resolution timing → statistical analysis
 *
 * Author: sectio-aurea-q / MEGALODON
 * License: MIT
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>

/* Kyber reference headers (linked via submodule) */
#include "api.h"
#include "kem.h"
#include "params.h"
#include "indcpa.h"
#include "randombytes.h"

/* ── Timing primitives ──────────────────────────────────── */

#if defined(__x86_64__) || defined(__i386__)
static inline uint64_t rdtsc_start(void) {
    unsigned int lo, hi;
    __asm__ volatile (
        "cpuid\n\t"
        "rdtsc\n\t"
        : "=a"(lo), "=d"(hi)
        :: "rbx", "rcx"
    );
    return ((uint64_t)hi << 32) | lo;
}

static inline uint64_t rdtsc_stop(void) {
    unsigned int lo, hi;
    __asm__ volatile (
        "rdtscp\n\t"
        "mov %%eax, %0\n\t"
        "mov %%edx, %1\n\t"
        "cpuid\n\t"
        : "=r"(lo), "=r"(hi)
        :: "rax", "rbx", "rcx", "rdx"
    );
    return ((uint64_t)hi << 32) | lo;
}
#else
/* Fallback: clock_gettime for non-x86 */
static inline uint64_t rdtsc_start(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + ts.tv_nsec;
}

static inline uint64_t rdtsc_stop(void) {
    return rdtsc_start();
}
#endif

/* ── Configuration ──────────────────────────────────────── */

#define NUM_MEASUREMENTS    10000
#define WARMUP_ROUNDS       500
#define OUTLIER_THRESHOLD   3.0   /* stddev multiplier for outlier removal */

/* Ciphertext mutation strategies */
typedef enum {
    MUTATE_NONE = 0,        /* baseline: valid ciphertext               */
    MUTATE_ZERO_CT,         /* all-zero ciphertext                      */
    MUTATE_FLIP_POLY,       /* flip bits in polynomial u                */
    MUTATE_FLIP_MSG,        /* flip bits in compressed message v        */
    MUTATE_RANDOM_CT,       /* fully random ciphertext                  */
    MUTATE_BOUNDARY_COEFF,  /* coefficients near decompression boundary */
    MUTATE_MAX
} mutation_t;

static const char *mutation_names[] = {
    "valid",
    "zero_ct",
    "flip_poly_u",
    "flip_msg_v",
    "random_ct",
    "boundary_coeff"
};

/* ── Data structures ────────────────────────────────────── */

typedef struct {
    uint64_t cycles[NUM_MEASUREMENTS];
    size_t   count;
    double   mean;
    double   median;
    double   stddev;
    double   min;
    double   max;
} timing_data_t;

/* ── Statistics ─────────────────────────────────────────── */

static int compare_u64(const void *a, const void *b) {
    uint64_t va = *(const uint64_t *)a;
    uint64_t vb = *(const uint64_t *)b;
    return (va > vb) - (va < vb);
}

static void compute_stats(timing_data_t *td) {
    if (td->count == 0) return;

    qsort(td->cycles, td->count, sizeof(uint64_t), compare_u64);

    td->min = (double)td->cycles[0];
    td->max = (double)td->cycles[td->count - 1];

    /* Median */
    if (td->count % 2 == 0) {
        td->median = (double)(td->cycles[td->count/2 - 1] +
                              td->cycles[td->count/2]) / 2.0;
    } else {
        td->median = (double)td->cycles[td->count/2];
    }

    /* Mean */
    double sum = 0.0;
    for (size_t i = 0; i < td->count; i++) {
        sum += (double)td->cycles[i];
    }
    td->mean = sum / (double)td->count;

    /* Stddev */
    double var = 0.0;
    for (size_t i = 0; i < td->count; i++) {
        double diff = (double)td->cycles[i] - td->mean;
        var += diff * diff;
    }
    td->stddev = sqrt(var / (double)td->count);
}

static size_t remove_outliers(timing_data_t *td) {
    compute_stats(td);
    double lo = td->mean - OUTLIER_THRESHOLD * td->stddev;
    double hi = td->mean + OUTLIER_THRESHOLD * td->stddev;

    size_t kept = 0;
    for (size_t i = 0; i < td->count; i++) {
        double v = (double)td->cycles[i];
        if (v >= lo && v <= hi) {
            td->cycles[kept++] = td->cycles[i];
        }
    }
    size_t removed = td->count - kept;
    td->count = kept;
    compute_stats(td);
    return removed;
}

/* ── Ciphertext mutation ────────────────────────────────── */

static void mutate_ciphertext(uint8_t *ct, size_t ct_len, mutation_t mut,
                              const uint8_t *original_ct) {
    memcpy(ct, original_ct, ct_len);

    switch (mut) {
    case MUTATE_NONE:
        /* Keep valid ciphertext as-is */
        break;

    case MUTATE_ZERO_CT:
        memset(ct, 0, ct_len);
        break;

    case MUTATE_FLIP_POLY:
        /* Flip bits in the first polynomial (u component) */
        for (size_t i = 0; i < KYBER_POLYVECCOMPRESSEDBYTES && i < ct_len; i += 32) {
            ct[i] ^= 0xFF;
        }
        break;

    case MUTATE_FLIP_MSG:
        /* Flip bits in the compressed message (v component) */
        if (ct_len > KYBER_POLYVECCOMPRESSEDBYTES) {
            size_t v_offset = KYBER_POLYVECCOMPRESSEDBYTES;
            for (size_t i = v_offset; i < ct_len; i += 16) {
                ct[i] ^= 0xFF;
            }
        }
        break;

    case MUTATE_RANDOM_CT:
        randombytes(ct, ct_len);
        break;

    case MUTATE_BOUNDARY_COEFF:
        /*
         * Set bytes near decompression boundaries.
         * Decompression: round(x * q / 2^d)
         * Boundary values cause the rounding to be ambiguous,
         * which may trigger different code paths.
         */
        for (size_t i = 0; i < ct_len; i++) {
            /* Values 0x7F and 0x80 sit at the compression midpoint */
            ct[i] = (i % 2 == 0) ? 0x7F : 0x80;
        }
        break;

    default:
        break;
    }
}

/* ── Core measurement ───────────────────────────────────── */

static void measure_decaps(const uint8_t *sk, const uint8_t *ct,
                           size_t ct_len, mutation_t mut,
                           const uint8_t *original_ct,
                           timing_data_t *td) {
    uint8_t mutated_ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss[CRYPTO_BYTES];
    uint64_t t0, t1;

    mutate_ciphertext(mutated_ct, ct_len, mut, original_ct);

    /* Warmup: populate caches, stabilize branch predictors */
    for (int i = 0; i < WARMUP_ROUNDS; i++) {
        crypto_kem_dec(ss, mutated_ct, sk);
    }

    /* Actual measurements */
    td->count = 0;
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        t0 = rdtsc_start();
        crypto_kem_dec(ss, mutated_ct, sk);
        t1 = rdtsc_stop();

        td->cycles[td->count++] = t1 - t0;
    }
}

/* ── CSV export ─────────────────────────────────────────── */

static int export_raw_csv(const char *filename, timing_data_t *data,
                          int num_mutations) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        perror("fopen");
        return -1;
    }

    /* Header */
    fprintf(fp, "measurement");
    for (int m = 0; m < num_mutations; m++) {
        fprintf(fp, ",%s", mutation_names[m]);
    }
    fprintf(fp, "\n");

    /* Data rows */
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        fprintf(fp, "%d", i);
        for (int m = 0; m < num_mutations; m++) {
            if ((size_t)i < data[m].count) {
                fprintf(fp, ",%lu", (unsigned long)data[m].cycles[i]);
            } else {
                fprintf(fp, ",");
            }
        }
        fprintf(fp, "\n");
    }

    fclose(fp);
    return 0;
}

static int export_summary_csv(const char *filename, timing_data_t *data,
                              int num_mutations) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        perror("fopen");
        return -1;
    }

    fprintf(fp, "mutation,count,mean,median,stddev,min,max\n");
    for (int m = 0; m < num_mutations; m++) {
        fprintf(fp, "%s,%zu,%.2f,%.2f,%.2f,%.2f,%.2f\n",
                mutation_names[m],
                data[m].count,
                data[m].mean,
                data[m].median,
                data[m].stddev,
                data[m].min,
                data[m].max);
    }

    fclose(fp);
    return 0;
}

/* ── Main ───────────────────────────────────────────────── */

int main(int argc, char **argv) {
    const char *raw_csv     = "data/timing_raw.csv";
    const char *summary_csv = "data/timing_summary.csv";

    if (argc > 1) raw_csv     = argv[1];
    if (argc > 2) summary_csv = argv[2];

    printf("╔══════════════════════════════════════════════════╗\n");
    printf("║  MEGALODON P1 — Timing Oracle on Kyber-512      ║\n");
    printf("║  Measurements per mutation: %d            ║\n", NUM_MEASUREMENTS);
    printf("║  Warmup rounds:             %d               ║\n", WARMUP_ROUNDS);
    printf("╚══════════════════════════════════════════════════╝\n\n");

    /* Key generation */
    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
    uint8_t ss[CRYPTO_BYTES];

    printf("[*] Generating Kyber-512 keypair...\n");
    if (crypto_kem_keypair(pk, sk) != 0) {
        fprintf(stderr, "[-] Key generation failed\n");
        return 1;
    }

    printf("[*] Encapsulating shared secret...\n");
    if (crypto_kem_enc(ct, ss, pk) != 0) {
        fprintf(stderr, "[-] Encapsulation failed\n");
        return 1;
    }

    /* Run measurements for each mutation strategy */
    timing_data_t results[MUTATE_MAX];
    memset(results, 0, sizeof(results));

    for (int m = 0; m < MUTATE_MAX; m++) {
        printf("[*] Measuring: %-20s ", mutation_names[m]);
        fflush(stdout);

        measure_decaps(sk, ct, CRYPTO_CIPHERTEXTBYTES,
                       (mutation_t)m, ct, &results[m]);

        size_t removed = remove_outliers(&results[m]);

        printf("→ mean=%.1f  median=%.1f  σ=%.1f  (-%zu outliers)\n",
               results[m].mean, results[m].median,
               results[m].stddev, removed);
    }

    /* Comparative analysis */
    printf("\n[*] Comparative Analysis (vs. valid baseline):\n");
    printf("    %-20s  %12s  %12s  %10s\n",
           "mutation", "Δ mean", "Δ median", "ratio");
    printf("    ────────────────────  ────────────  ────────────  ──────────\n");

    for (int m = 1; m < MUTATE_MAX; m++) {
        double d_mean   = results[m].mean - results[0].mean;
        double d_median = results[m].median - results[0].median;
        double ratio    = results[m].mean / results[0].mean;

        printf("    %-20s  %+12.1f  %+12.1f  %10.6f\n",
               mutation_names[m], d_mean, d_median, ratio);
    }

    /* Export */
    printf("\n[*] Exporting raw timing data → %s\n", raw_csv);
    if (export_raw_csv(raw_csv, results, MUTATE_MAX) != 0) {
        fprintf(stderr, "[-] Failed to export raw CSV\n");
    }

    printf("[*] Exporting summary → %s\n", summary_csv);
    if (export_summary_csv(summary_csv, results, MUTATE_MAX) != 0) {
        fprintf(stderr, "[-] Failed to export summary CSV\n");
    }

    /* Verdict */
    printf("\n[*] Timing differential detected: ");
    double max_ratio = 0.0;
    int max_mut = 0;
    for (int m = 1; m < MUTATE_MAX; m++) {
        double ratio = fabs(results[m].mean - results[0].mean) / results[0].stddev;
        if (ratio > max_ratio) {
            max_ratio = ratio;
            max_mut = m;
        }
    }

    if (max_ratio > 2.0) {
        printf("YES — '%s' shows %.2fσ deviation\n",
               mutation_names[max_mut], max_ratio);
        printf("    ⚠  Potential timing side-channel in decapsulation\n");
    } else if (max_ratio > 1.0) {
        printf("WEAK — '%s' shows %.2fσ deviation (needs more samples)\n",
               mutation_names[max_mut], max_ratio);
    } else {
        printf("NO — Implementation appears timing-constant (max %.2fσ)\n",
               max_ratio);
    }

    printf("\n[*] Done. Run analysis/visualize.py on the CSV for plots.\n");
    return 0;
}
