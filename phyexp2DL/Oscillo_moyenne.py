"""Valeur moyenne d'un signal périodique : égalité des aires sur une période."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,
                     'mathtext.fontset':'dejavusans','svg.fonttype':'none'})
blue, magenta, gray = '#28618A','#C020A0','#41464B'
T, t0, mean = 1.0, .18, 1.35

def signal(t):
    return mean + .60*np.cos(2*np.pi*t) + .23*np.sin(4*np.pi*t+.5)

t=np.linspace(-.12,1.55,1500)
inside=np.linspace(t0,t0+T,1000)
fig,axes=plt.subplots(1,2,figsize=(12,5.1))
fig.subplots_adjust(left=.065,right=.97,bottom=.12,top=.88,wspace=.18)
for ax in axes:
    ax.set(xlim=(-.16,1.62),ylim=(-.45,2.65))
    ax.axis('off')
    ax.annotate('',(1.6,0),(-.13,0),arrowprops=dict(arrowstyle='->',lw=1.3,color=gray))
    ax.annotate('',(0,2.50),(0,-.07),arrowprops=dict(arrowstyle='->',lw=1.3,color=gray))
    ax.text(-.035,2.54,'$s(t)$',ha='center',va='bottom',fontsize=18)
    ax.text(1.61,-.045,'$t$',ha='center',va='top',fontsize=18)
    ax.text(-.035,-.025,'$0$',ha='right',va='top',fontsize=12)
    for x,label in [(t0,'$t_0$'),(t0+T,'$t_0+T$')]:
        ax.vlines(x,0,2.30,color='#8D969E',linestyle=':',lw=1)
        ax.text(x,-.085,label,ha='center',va='top',fontsize=15)
    ax.annotate('',(t0+T,-.33),(t0,-.33),arrowprops=dict(arrowstyle='<->',lw=1.4,color=gray,shrinkA=0,shrinkB=0))
    ax.text(t0+T/2,-.35,'$T$',ha='center',va='top',fontsize=16)
    ax.hlines(mean,-.07,1.51,linestyle=(0,(5,4)),color=magenta,lw=1.5)
    ax.text(-.09,mean,r'$\bar{s}$',color=magenta,ha='right',va='center',fontsize=19)

axes[0].fill_between(inside,0,signal(inside),color=blue,alpha=.18,zorder=0)
axes[0].plot(t,signal(t),color=blue,lw=2.5)
axes[0].text(.69,.35,r'$\int_{t_0}^{t_0+T} s(t)\,\mathrm{d}t$',color=blue,ha='center',fontsize=18)
axes[1].plot(t,signal(t),color='#AAB4BE',lw=1.4,zorder=1)
axes[1].fill_between(inside,0,mean,color=magenta,alpha=.12,zorder=0)
axes[1].plot([t0,t0,t0+T,t0+T],[0,mean,mean,0],color=magenta,lw=1.8,zorder=3)
axes[1].text(.68,.58,r'$T\,\bar{s}$',color=magenta,ha='center',fontsize=23)
axes[0].set_title('Aire sous le signal',fontsize=17,color=gray,pad=15)
axes[1].set_title('Rectangle de même aire',fontsize=17,color=gray,pad=15)
out=Path(__file__).resolve().parent
for ext in ('png','svg','pdf'):
    fig.savefig(out/f'valeur_moyenne.{ext}',dpi=220,bbox_inches='tight',facecolor='white',pad_inches=.18)
print(out/'valeur_moyenne.png')
