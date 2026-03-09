# MEGALODON P1 — Disassembly Analysis

## Finding

The FO-transformation in crypto_kem_dec is architecturally branchless:
- verify() uses NEON SIMD (eor/orr) — no secret-dependent branches
- cmov() uses ARM NEON bit instructions — no secret-dependent branches
- cset w3, eq is a branchless conditional set

## Root Cause of Timing Leak

The leak does NOT originate from verify/cmov. It originates from
indcpa_enc() (re-encryption step at 0x100001864).

When decapsulating a valid ciphertext, the decrypted message is
meaningful polynomial data. When decapsulating a mutated ciphertext,
the decrypted message is pseudorandom garbage.

The re-encryption of these different messages causes:
1. Different cache-line access patterns in NTT/polynomial multiplication
2. Different branch predictor states from loop-internal data patterns
3. Measurable 1200-1500ns timing differential (Cohen d = 0.63-0.73)

## Implications

- The ref/ implementation is NOT constant-time despite branchless verify/cmov
- The leak is microarchitectural, not architectural
- Exploitation requires local/co-located attacker with high-precision timing
- Standard countermeasure: constant-time polynomial arithmetic (see pqm4, PQClean)

## Key Instructions (from objdump)

    crypto_kem_dec:
      0x100001864: bl indcpa_enc        ; re-encrypt decrypted message
      0x100001874: bl verify            ; compare CT with re-encrypted CT
      0x10000188c: cmp w22, #0x0        ; check verify result
      0x100001890: cset w3, eq          ; branchless condition bit
      0x1000018a0: bl cmov              ; branchless conditional copy
