#!/usr/bin/env python3
"""MEGALODON P1 — Statistical Side-Channel Analysis"""
import argparse,os,csv,numpy as np
from scipy import stats

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
    with open(a.raw) as f:
        reader=csv.DictReader(f)
        cols={h:[] for h in reader.fieldnames if h!='measurement'}
        for row in reader:
            for h in cols:
                cols[h].append(float(row[h]))
    t={k:np.array(v) for k,v in cols.items()}
    bl_name='valid'
    baseline=t[bl_name]
    mutations=[k for k in t if k!=bl_name]
    alpha=0.01
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  MEGALODON P1 — Statistical Side-Channel Analysis                          ║")
    print("║  Baseline: %-20s  Samples: %-10d  α = %.2f             ║"%(bl_name,len(baseline),alpha))
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    hdr=f"{'Mutation':<18} {'Welch t':>10} {'p-value':>12} {'KS stat':>10} {'KS p':>12} {'Cohen d':>10} {'99% CI Δ (ns)':>20} {'Sig?':>6}"
    print(hdr); print("─"*len(hdr))
    results=[]
    any_sig=False
    for m in mutations:
        x=t[m]
        t_stat,t_p=stats.ttest_ind(baseline,x,equal_var=False)
        ks_stat,ks_p=stats.ks_2samp(baseline,x)
        d=cohens_d(baseline,x)
        diff=np.mean(baseline)-np.mean(x)
        se=np.sqrt(np.var(baseline,ddof=1)/len(baseline)+np.var(x,ddof=1)/len(x))
        z=stats.norm.ppf(0.995)
        ci_lo,ci_hi=diff-z*se,diff+z*se
        sig="YES" if t_p<alpha else "NO"
        if t_p<alpha: any_sig=True
        print(f"{m:<18} {t_stat:>10.3f} {t_p:>12.2e} {ks_stat:>10.4f} {ks_p:>12.2e} {d:>10.4f} {'[%+.1f, %+.1f]'%(ci_lo,ci_hi):>20} {sig:>6}")
        results.append((m,t_stat,t_p,ks_stat,ks_p,d,ci_lo,ci_hi,sig))
    print()
    if any_sig: print("[!] TIMING DIFFERENTIAL DETECTED")
    else: print("[✓] NO significant timing differential at α=%.2f"%alpha)
    md=os.path.join(a.outdir,'stats_results.md')
    with open(md,'w') as f:
        f.write("# MEGALODON P1 — Statistical Analysis Results\n\n")
        f.write("**Baseline:** `%s` | **Samples:** %d | **α:** %.2f\n\n"%(bl_name,len(baseline),alpha))
        f.write("| Mutation | Welch t | p-value | KS stat | KS p | Cohen's d | 99%% CI Δ (ns) | Significant? |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for m,ts,tp,ks,kp,d,cl,ch,sg in results:
            f.write("| %s | %.3f | %.2e | %.4f | %.2e | %.4f | [%+.1f, %+.1f] | %s |\n"%(m,ts,tp,ks,kp,d,cl,ch,sg))
        f.write("\n**%s**\n"%("⚠ TIMING DIFFERENTIAL DETECTED" if any_sig else "✓ No significant timing differential. Implementation appears constant-time."))
    csv_out=os.path.join(a.outdir,'stats_results.csv')
    with open(csv_out,'w') as f:
        f.write("mutation,welch_t,welch_p,ks_stat,ks_p,cohens_d,ci99_lo,ci99_hi,significant\n")
        for m,ts,tp,ks,kp,d,cl,ch,sg in results:
            f.write("%s,%.6f,%.2e,%.6f,%.2e,%.6f,%.2f,%.2f,%s\n"%(m,ts,tp,ks,kp,d,cl,ch,sg))
    print(f"\n[*] → {md}\n[*] → {csv_out}")

if __name__=='__main__': main()
