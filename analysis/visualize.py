#!/usr/bin/env python3
import argparse, os, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

C_BG='#0a0a0f'; C_GRID='#1a1a2e'; C_TEXT='#c0c0d0'
C_ACCENT=['#00ff88','#ff3366','#ff9933','#6633ff','#33ccff','#ffcc00']

def style(ax):
    ax.set_facecolor(C_BG)
    ax.tick_params(colors=C_TEXT)
    ax.xaxis.label.set_color(C_TEXT); ax.yaxis.label.set_color(C_TEXT)
    ax.title.set_color(C_TEXT)
    for s in ax.spines.values(): s.set_color(C_GRID)
    ax.grid(True,color=C_GRID,alpha=0.4)

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

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--raw',required=True)
    pa.add_argument('--outdir',required=True)
    a=pa.parse_args()
    os.makedirs(a.outdir,exist_ok=True)
    t=load(a.raw)
    if not t: print("No data!"); exit(1)
    labels=list(t.keys()); vals=[t[l] for l in labels]
    # Boxplots
    fig,ax=plt.subplots(figsize=(12,6)); fig.patch.set_facecolor(C_BG); style(ax)
    bp=ax.boxplot(vals,labels=labels,patch_artist=True,showfliers=False,widths=0.6,medianprops=dict(color='white',linewidth=2))
    for i,p in enumerate(bp['boxes']): p.set_facecolor(C_ACCENT[i%6]); p.set_alpha(0.7); p.set_edgecolor('white')
    for e in ['whiskers','caps']:
        for l in bp[e]: l.set_color(C_TEXT)
    ax.set_title('MEGALODON P1 — Decapsulation Timing',fontsize=14,fontweight='bold')
    ax.set_ylabel('Time (ns)'); ax.set_xticklabels(labels,rotation=25,ha='right',fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir,'boxplots.png'),dpi=150,facecolor=C_BG); plt.close()
    # Histograms
    fig,ax=plt.subplots(figsize=(12,6)); fig.patch.set_facecolor(C_BG); style(ax)
    av=np.concatenate(vals); lo,hi=np.percentile(av,1),np.percentile(av,99); bins=np.linspace(lo,hi,80)
    for i,(l,ns) in enumerate(t.items()): ax.hist(ns,bins=bins,alpha=0.45,color=C_ACCENT[i%6],label=l,edgecolor='none')
    ax.set_title('MEGALODON P1 — Timing Distribution',fontsize=14,fontweight='bold')
    ax.set_xlabel('Time (ns)'); ax.set_ylabel('Count')
    ax.legend(fontsize=8,facecolor=C_BG,edgecolor=C_GRID,labelcolor=C_TEXT)
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir,'histograms.png'),dpi=150,facecolor=C_BG); plt.close()
    # Heatmap
    fig,ax=plt.subplots(figsize=(12,5)); fig.patch.set_facecolor(C_BG); style(ax)
    edges=np.percentile(av,np.linspace(0,100,11))
    mx=np.zeros((len(labels),10))
    for i,l in enumerate(labels):
        c,_=np.histogram(t[l],bins=edges); s=c.sum(); mx[i,:]=c/s if s>0 else 0
    ax.imshow(mx,aspect='auto',cmap='inferno',interpolation='nearest')
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels,fontsize=9)
    bl=[f'{edges[j]:.0f}-{edges[j+1]:.0f}' for j in range(10)]
    ax.set_xticks(range(10)); ax.set_xticklabels(bl,rotation=45,ha='right',fontsize=7)
    ax.set_title('MEGALODON P1 — Timing Heatmap',fontsize=14,fontweight='bold')
    fig.tight_layout(); fig.savefig(os.path.join(a.outdir,'heatmap.png'),dpi=150,facecolor=C_BG); plt.close()
    print("Done:",os.listdir(a.outdir))

if __name__=='__main__': main()
