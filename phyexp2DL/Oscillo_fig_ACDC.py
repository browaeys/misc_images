"""Décomposition d'une tension périodique en composantes DC et AC."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'mathtext.fontset':'dejavusans','svg.fonttype':'none'})
blue, magenta, gray = '#28618A','#C020A0','#41464B'
t=np.linspace(0,2.35,1400)
dc=1.30
ac=.66*np.cos(2*np.pi*t+.35)+.17*np.sin(4*np.pi*t+.4)
fig, axes=plt.subplots(1,3,figsize=(13,4.6))
fig.subplots_adjust(left=.045,right=.98,bottom=.09,top=.82,wspace=.28)
for ax in axes:
    ax.set(xlim=(-.19,2.57),ylim=(-1.05,2.48))
    ax.axis('off')
    ax.annotate('',(2.51,0),(-.08,0),arrowprops=dict(arrowstyle='->',color=gray,lw=1.2))
    ax.annotate('',(0,2.38),(0,-.95),arrowprops=dict(arrowstyle='->',color=gray,lw=1.2))
    ax.text(2.53,-.08,'$t$',fontsize=17,ha='center',va='top')
    ax.text(-.06,-.06,'$0$',fontsize=12,ha='right',va='top',color=gray)
axes[0].plot(t,dc+ac,color=blue,lw=2.6)
axes[0].hlines(dc,0,2.35,color=magenta,linestyle=(0,(5,4)),lw=1.6)
axes[0].text(-.10,dc,r'$U^{\mathrm{DC}}=\langle u\rangle$',color=magenta,fontsize=15,ha='right',va='center',
             bbox=dict(facecolor='white',edgecolor='none',pad=1.5))
axes[1].plot([0,2.35],[dc,dc],color=magenta,lw=2.6)
axes[1].text(1.17,dc+.20,r'$U^{\mathrm{DC}}=\langle u\rangle$',color=magenta,fontsize=18,ha='center')
axes[2].plot(t,ac,color=blue,lw=2.6)
# Les trois panneaux ont les mêmes échelles temporelle et verticale.
for ax,title,color in zip(axes,[r'$u(t)$',r'$U^{\mathrm{DC}}$',r'$u^{\mathrm{AC}}(t)$'],[blue,magenta,blue]):
    ax.set_title(title,fontsize=23,color=color,pad=20)
for ax,caption in zip(axes,['Signal complet','Composante continue','Composante alternative']):
    ax.text(.5,1.015,caption,transform=ax.transAxes,ha='center',va='bottom',fontsize=12,color=gray)
# Décomposition lisible directement entre les panneaux.
for a,b,sign in [(axes[0],axes[1],'='),(axes[1],axes[2],'+')]:
    left,right=a.get_position(),b.get_position()
    fig.text((left.x1+right.x0)/2,.49,sign,fontsize=30,color=gray,ha='center',va='center')
axes[2].text(1.18,1.53,r'$\langle u^{\mathrm{AC}}\rangle=0$',color=blue,fontsize=18,ha='center')
out=Path(__file__).resolve().parent
for ext in ('png','svg','pdf'):
    fig.savefig(out/f'composantes_ac_dc.{ext}',dpi=220,bbox_inches='tight',facecolor='white',pad_inches=.18)
print(out/'composantes_ac_dc.png')
