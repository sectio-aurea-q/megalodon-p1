#!/usr/bin/env python3
"""MEGALODON P1 — Compare ref vs aarch64 implementation timing"""
import csv,os,numpy as np
from scipy import stats

def load_csv(path):
    data={}
    with open(path) as f:
        reader=csv.reader(f)
        headers=next(reader)
        for h in headers:
            h=h.strip()
            if h and h!='measurement': data[h]=[]
        for row in reader:
            for i,h in enumerate(headers):
                h=h.strip()
                if h and h!='measurement' and i<len(row):
                    val=row[i].strip()
                    if val:
                        try: data[h].append(float(val))
                        except: pass
    return {k:np.array(v) for k,v in data.items() if len(v)>0}

def analyze(name,t):
    bl=t.get('valid',list(t.values())[0])
    bl_name='valid'
    mutations=[k for k in t if k!=bl_name]
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"  Baseline mean: {np.mean(bl):.1f} ns  median: {np.median(bl):.1f} ns  std: {np.std(bl):.1f}")
    print(f"{'='*70}")
    print(f"  {'Mutation':<18} {'mean':>10} {'Cohen d':>10} {'p-value':>12} {'Sig?':>6}")
    print(f"  {'-'*60}")
    any_sig=False
    for m in mutations:
        x=t[m]
        t_stat,t_p=stats.ttest_ind(bl,x,equal_var=False)
        na,nb=len(bl),len(x)
        sp=np.sqrt(((na-1)*np.var(bl,ddof=1)+(nb-1)*np.var(x,ddof=1))/(na+nb-2))
        d=(np.mean(bl)-np.mean(x))/sp if sp>0 else 0
        sig="YES" if t_p<0.01 else "NO"
        if t_p<0.01: any_sig=True
        print(f"  {m:<18} {np.mean(x):>10.1f} {d:>10.4f} {t_p:>12.2e} {sig:>6}")
    return any_sig

def main():
    ref_path='data/timing_raw.csv'
    arm_path='data/timing_aarch64.csv'
    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║  MEGALODON P1 — Implementation Comparison: ref vs aarch64      ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    ref=load_csv(ref_path)
    ref_sig=analyze("REFERENCE (ref/) — not hardened",ref)
    if os.path.exists(arm_path):
        arm=load_csv(arm_path)
        arm_sig=analyze("AARCH64 (aarch64/) — NEON hardened",arm)
        print(f"\n{'='*70}")
        print("  VERDICT")
        print(f"{'='*70}")
        print(f"  ref/     timing leak: {'YES — CONFIRMED' if ref_sig else 'NO'}")
        print(f"  aarch64/ timing leak: {'YES — CONFIRMED' if arm_sig else 'NO'}")
        if ref_sig and not arm_sig:
            print("\n  >> Hardened aarch64 implementation mitigates the timing leak.")
            print("  >> This confirms the ref/ leak is real and the countermeasure works.")
        elif ref_sig and arm_sig:
            print("\n  >> BOTH implementations leak. Potential novel finding.")
        else:
            print("\n  >> Neither implementation shows significant timing differential.")
        # Side by side std comparison
        print(f"\n  Timing variance comparison (std of valid baseline):")
        print(f"    ref/:     {np.std(ref['valid']):.1f} ns")
        print(f"    aarch64/: {np.std(arm['valid']):.1f} ns")
    else:
        print(f"\n  [!] {arm_path} not found. Run: make run-aarch64")

if __name__=='__main__': main()
