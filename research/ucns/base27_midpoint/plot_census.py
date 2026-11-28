"""Optional visual and CSV export. Usage: python plot_census.py (matplotlib for plot)."""
import csv
import json
from pathlib import Path

root=Path(__file__).parent
r=json.loads((root/'evidence.json').read_text())['prime_census']
a,b=(r[k]['all_output_families'] for k in ('first_interval','next_interval'))
with (root/'brightness.csv').open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['output_spoke','first_family_0','first_family_1','first_family_2','first_total','next_family_0','next_family_1','next_family_2','next_total'])
    for x,y in zip(a,b,strict=True):
        if x['output_spoke']!=y['output_spoke']:
            raise ValueError('spoke mismatch')
        w.writerow([x['output_spoke'],*x['family_counts'],x['total'],*y['family_counts'],y['total']])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
colors=['#377da0','#edaa47','#8063ae']
fig,axs=plt.subplots(2,1,figsize=(12,6.6),sharex=True,sharey=True)
for ax,rows,title in zip(axs,(a,b),('First window: upper prime ≤ 30,000,000  |  5,646 pairs','Next window: 30,000,000 < lower prime; upper prime ≤ 60,000,000  |  4,721 pairs'),strict=True):
    bottom=[0]*81
    for j in range(3):
        vals=[x['family_counts'][j] for x in rows]
        ax.bar(range(81),vals,bottom=bottom,width=.84,color=colors[j],label=f'Input family {j}')
        bottom=[p+q for p,q in zip(bottom,vals)]
    ax.set_title(title,loc='left',fontsize=10,weight='bold')
    ax.set_ylabel('Twin pairs')
    ax.grid(axis='y',alpha=.20)
    ax.set_axisbelow(True)
    ax.set_ylim(0,95)
    ax.spines[['top','right']].set_visible(False)
axs[0].legend(ncol=3,loc='upper right',frameon=False,fontsize=8)
axs[1].xaxis.set_major_locator(MultipleLocator(10))
axs[1].set_xlabel('Output spoke index  (multiply by 243 for residue)')
fig.suptitle('Base-27 twin-prime cubing: all 81 output spokes × three input families',fontsize=14,weight='bold',x=.5,y=.98)
fig.text(.5,.01,'Counts are descriptive integer-residue frequencies, not security or entropy estimates.',ha='center',fontsize=9,color='#454545')
fig.tight_layout(rect=(0,.04,1,.95))
fig.savefig(root/'brightness.png',dpi=160,bbox_inches='tight')
