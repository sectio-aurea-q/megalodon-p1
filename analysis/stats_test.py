#!/usr/bin/env python3
"""
MEGALODON P1 — Statistical Side-Channel Analysis
Welch's t-test, Kolmogorov-Smirnov, Cohen's d, 99% CI
"""
import argparse, os, numpy as np
from scipy import stats

def load(path):
    d={}
    with open(path) as f:
        f.readline()
        for line in f:
            p=line.strip().split(',')
            if len(p)<3: continue
            m=p[0].strip()
            try: ns=float(p[2].strip())
            except: continue
            d.setdefault(m,[]).append(ns)
    return {k:np.array(v) for k,v in d.items()}

def cohens_d(a,b):
    na,nb=len(a),len(b)
    sp=np.sqrt(((na-1)*np.var(a,ddof=1)+(nb-1)*np.var(b,ddof=1))/(na+nb-2))
    return (np.mean(a)-np.mean(b))/sp if sp>0 else 0.0

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--raw',required=True)
    pa.add_argument('--outdir',required=True)
    a=pa.parse_args()
    os.makedirs(a.outdir,exist_ok=True)

    t=load(a.raw)
    if not t: print("No data!"); exit(1)

    mutations=[k for k in t.keys() if k!='valid']
    baseline=t.get('valid')
    if baseline is None:
        baseline=list(t.values())[0]
        bl_name=list(t.keys())[0]
    else:
        bl_name='valid'

    alpha=0.01
    ci_level=0.99

    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  MEGALODON P1 — Statistical Side-Channel Analysis                          ║")
    print("║  Baseline: %-20s  Samples: %-10d  α = %.2f             ║" % (bl_name, len(baseline), alpha))
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    hdr=f"{'Mutation':<18} {'Welch t':>10} {'p-value':>12} {'KS stat':>10} {'KS p':>12} {'Cohen d':>10} {'99% CI Δ (ns)':>20} {'Sig?':>6}"
    print(hdr)
    print("─"*len(hdr))

    results=[]
    any_sig=False

    for m in mutations:
        x=t[m]
        # Welch's t-test
        t_stat,t_p=stats.ttest_ind(baseline,x,equal_var=False)
        # KS test
        ks_stat,ks_p=stats.ks_2samp(baseline,x)
        # Cohen's d
        d=cohens_d(baseline,x)
        # 99% CI for mean difference
        diff=np.mean(baseline)-np.mean(x)
        se=np.sqrt(np.var(baseline,ddof=1)/len(baseline)+np.var(x,ddof=1)/len(x))
        z=stats.norm.ppf((1+ci_level)/2)
        ci_lo=diff-z*se
        ci_hi=diff+z*se
        sig="YES" if t_p<alpha else "NO"
        if t_p<alpha: any_sig=True

        print(f"{m:<18} {t_stat:>10.3f} {t_p:>12.2e} {ks_stat:>10.4f} {ks_p:>12.2e} {d:>10.4f} {'[%+.1f, %+.1f]'%(ci_lo,ci_hi):>20} {sig:>6}")
        results.append((m,t_stat,t_p,ks_stat,ks_p,d,ci_lo,ci_hi,sig))

    print()
    if any_sig:
        print("[!] TIMING DIFFERENTIAL DETECTED — potential side-channel leakage")
    else:
        print("[✓] NO significant timing differential at α=%.2f — implementation appears constant-time" % alpha)

    # Export markdown table
    md=os.path.join(a.outdir,'stats_results.md')
    with open(md,'w') as f:
        f.write("# MEGALODON P1 — Statistical Analysis Results\n\n")
        f.write("**Baseline:** `%s` | **Samples:** %d | **Significance level:** α = %.2f\n\n" % (bl_name,len(baseline),alpha))
        f.write("| Mutation | Welch t | p-value | KS stat | KS p | Cohen's d | 99%% CI Δ (ns) | Significant? |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for m,ts,tp,ks,kp,d,cl,ch,sg in results:
            f.write("| %s | %.3f | %.2e | %.4f | %.2e | %.4f | [%+.1f, %+.1f] | %s |\n" % (m,ts,tp,ks,kp,d,cl,ch,sg))
        f.write("\n")
        if any_sig:
            f.write("**⚠ TIMING DIFFERENTIAL DETECTED**\n")
        else:
            f.write("**✓ No significant timing differential detected. Implementation appears constant-time.**\n")

    # Export CSV
    csv=os.path.join(a.outdir,'stats_results.csv')
    with open(csv,'w') as f:
        f.write("mutation,welch_t,welch_p,ks_stat,ks_p,cohens_d,ci99_lo,ci99_hi,significant\n")
        for m,ts,tp,ks,kp,d,cl,ch,sg in results:
            f.write("%s,%.6f,%.2e,%.6f,%.2e,%.6f,%.2f,%.2f,%s\n" % (m,ts,tp,ks,kp,d,cl,ch,sg))

    print(f"\n[*] Results exported → {md}")
    print(f"[*] Results exported → {csv}")

if __name__=='__main__': main()
