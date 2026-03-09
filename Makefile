# ═══════════════════════════════════════════════════════
# MEGALODON P1 — Timing Oracle on CRYSTALS-Kyber
# ═══════════════════════════════════════════════════════

CC        = gcc
CFLAGS    = -O2 -Wall -Wextra -Wpedantic -march=native
LDFLAGS   = -lm

# Kyber reference implementation (submodule)
KYBER_DIR  = kyber/ref
KYBER_SRCS = $(KYBER_DIR)/kem.c \
             $(KYBER_DIR)/indcpa.c \
             $(KYBER_DIR)/polyvec.c \
             $(KYBER_DIR)/poly.c \
             $(KYBER_DIR)/ntt.c \
             $(KYBER_DIR)/cbd.c \
             $(KYBER_DIR)/reduce.c \
             $(KYBER_DIR)/verify.c \
             $(KYBER_DIR)/symmetric-shake.c \
             $(KYBER_DIR)/fips202.c \
             $(KYBER_DIR)/randombytes.c

# Kyber security level (512, 768, or 1024)
KYBER_K   ?= 2
DEFINES    = -DKYBER_K=$(KYBER_K)

INCLUDES   = -I$(KYBER_DIR)
SRC        = src/timing_oracle.c
TARGET     = timing_oracle

# ── Targets ────────────────────────────────────────────

.PHONY: all clean run setup plot kyber512 kyber768 kyber1024

all: $(TARGET)

$(TARGET): $(SRC) $(KYBER_SRCS)
	@echo "[BUILD] Compiling timing oracle (KYBER_K=$(KYBER_K))..."
	$(CC) $(CFLAGS) $(DEFINES) $(INCLUDES) -o $@ $^ $(LDFLAGS)
	@echo "[BUILD] Done → ./$(TARGET)"

# Convenience targets for different security levels
kyber512:
	$(MAKE) KYBER_K=2 TARGET=timing_oracle_512

kyber768:
	$(MAKE) KYBER_K=3 TARGET=timing_oracle_768

kyber1024:
	$(MAKE) KYBER_K=4 TARGET=timing_oracle_1024

run: $(TARGET)
	@mkdir -p data
	./$(TARGET) data/timing_raw.csv data/timing_summary.csv

plot:
	@echo "[PLOT] Generating visualizations..."
	python3 analysis/visualize.py --raw data/timing_raw.csv --outdir data/plots

setup:
	@echo "[SETUP] Cloning Kyber reference implementation..."
	@if [ ! -d "kyber" ]; then \
		git clone https://github.com/pq-crystals/kyber.git; \
	else \
		echo "[SETUP] kyber/ already exists"; \
	fi
	@echo "[SETUP] Installing Python dependencies..."
	pip3 install matplotlib scipy numpy --quiet
	@echo "[SETUP] Done. Run 'make' to build."

clean:
	rm -f timing_oracle timing_oracle_512 timing_oracle_768 timing_oracle_1024
	rm -rf data/plots data/timing_raw.csv data/timing_summary.csv

# ── Full pipeline ──────────────────────────────────────

pipeline: setup all run plot
	@echo "[PIPELINE] Complete. Check data/plots/ for results."
