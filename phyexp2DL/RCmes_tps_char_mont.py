"""Montée non exponentielle : définitions graphiques des temps caractéristiques."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib-rcmes')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(figsize=(11, 7.8))
fig.subplots_adjust(left=.105, right=.965, top=.94, bottom=.36)
blue, orange, purple, green = '#1764a0', '#c66b13', '#c42b38', '#19816b'
# La pente évolue d'abord à la hausse, puis à la baisse : ce n'est pas
# une réponse exponentielle simple. La pente initiale est 0,4 ; au temps de tangente, le signal vaut environ 95 %.
def response(t):
    return 1 - np.exp(-.4*t - .32*t**2)
def crossing(p):
    return (-.4 + np.sqrt(.4**2 - 1.28*np.log(1-p))) / .64
th, t10, t90, t63 = [crossing(p) for p in [.5, .1, .9, .63]]
ttan = 2.5
t = np.linspace(0, 5, 1000)
ax.plot(t, response(t), color='#303438', lw=3, zorder=4)
ax.axhline(1, color='#63717c', lw=1.1, ls=(0,(3,3)), alpha=.8)
ax.plot([0,ttan*1.08], [0,1.08], color=green, lw=1.1, ls=(0,(5,3)))
ax.scatter([ttan],[1], s=65, facecolors='white', edgecolors=green, linewidths=2, zorder=6)
ax.text(1.7,.57,'Tangente à l’origine', color=green, fontsize=12,
        rotation=40, rotation_mode='anchor')
ax.set_xlim(0,5)
ax.set_ylim(0,1.13)
ax.set_yticks([0,.1,.5,.63,.9,1], ['0','10 %','50 %',r'$\alpha$','90 %','100 %'])
ax.set_xticks([0], ['0'])
ax.set_xlabel('Temps', loc='right', labelpad=8)
ax.text(-.075, 1.025, 'Signal quelconque', transform=ax.transAxes, ha='left')
ax.spines[['left','bottom']].set_visible(False)
# Axes fléchés, indépendants des repères de construction.
for endpoint in [(1.015, 0), (0, 1.015)]:
    ax.annotate('', xy=endpoint, xytext=(0, 0), xycoords='axes fraction',
                arrowprops=dict(arrowstyle='-|>', color='#7d8790', lw=1.1,
                                mutation_scale=13, shrinkA=0, shrinkB=0),
                annotation_clip=False, zorder=2)
ax.tick_params(color='#a1aab2')
trans = ax.get_xaxis_transform()
def guide(x,level,row,color):
    ax.plot([0,x],[level,level], color=color, lw=1.1, ls=(0,(3,3)), alpha=.8)
    ax.plot([x,x],[level/ax.get_ylim()[1],row], transform=trans,
            color=color, lw=1.1, ls=(0,(3,3)), alpha=.8, clip_on=False)
    ax.scatter([x],[level], s=40, color=color, zorder=6)
def interval(a,b,row,color,label):
    ax.annotate('',xy=(a,row),xytext=(b,row),xycoords=trans,
                arrowprops=dict(arrowstyle='<->',color=color,lw=1.9),annotation_clip=False)
    for x in [a,b]:
        ax.plot([x,x],[row-.018,row+.018],transform=trans,color=color,lw=1.2,clip_on=False)
    ax.text((a+b)/2,row+.010,label,transform=trans,ha='center',va='bottom',
            color=color,fontsize=14,clip_on=False,
            bbox=dict(facecolor='white',edgecolor='none',pad=1.5))
# Les projections se prolongent jusqu'à la flèche propre à chaque définition.
for x,level,row,color in [(th,.5,-.17,purple),(t10,.1,-.29,orange),
                           (t90,.9,-.29,orange),(t63,.63,-.41,blue)]:
    guide(x,level,row,color)
ax.plot([ttan,ttan],[1/1.13,-.53], transform=trans, color=green,
        lw=1.1, ls=(0,(3,3)), alpha=.8, clip_on=False)
ax.plot([0,0],[0,-.53],transform=trans,color='#9aa4ad',lw=1,
        ls=(0,(3,3)),clip_on=False)
interval(0,th,-.17,purple,r'$t_{1/2}$')
interval(t10,t90,-.29,orange,r'$t_{10–90}$')
interval(0,t63,-.41,blue,r'$t_{\alpha}$')
interval(0,ttan,-.53,green,r'$t_{\mathrm{tangente}}$')
for ext in ['png','svg']:
    fig.savefig(out/f'{Path(__file__).stem}.{ext}', dpi=200, facecolor='white')
plt.close(fig)
print(f't1/2={th:.3f}, t10–90={t90-t10:.3f}, t63={t63:.3f}, ttangente={ttan:.3f}')
