"""Charge d'un condensateur initialement déchargé : échelon de 0 à E."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib-rcmes')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

out = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13})
fig, ax = plt.subplots(figsize=(8, 5.5))
fig.subplots_adjust(left=.09, right=.97, bottom=.32, top=.84)
ink, red, grey = '#000000', '#c42b38', '#7d8790'
green = '#19816b'
guide_style = dict(color='#b7bec4', lw=.9, ls=(0, (2, 4)))
E, tau = 1., 1.
ax.set_xlim(-1.3, 5.7)
ax.set_ylim(-.06, 1.22)
ax.spines[:].set_visible(False)
ax.set_xticks([0], ['0'])
ax.set_yticks([E], [r'$E$'])
ax.tick_params(length=0, pad=9)
for end in [(5.7, 0), (-1.3, 1.2)]:
    ax.annotate('', xy=end, xytext=(-1.3, 0),
                arrowprops=dict(arrowstyle='-|>', color=grey, lw=1.1),
                annotation_clip=False, zorder=1)
ax.text(5.7, -.045, r'$t$', ha='right', va='top', fontsize=17)
ax.text(-1.3, 1.23, 'Tension', ha='left', fontsize=13)
ax.axhline(E, **guide_style)
ax.plot([0, 0], [0, 1.06], **guide_style)
# L'entrée est tracée sous la réponse, y compris sur le palier initial.
ax.plot([-1.3, 0, 0, 5.5], [0, 0, E, E], color=red, lw=4,
        zorder=3, solid_capstyle='butt')
ax.plot([-1.3, 0], [0, 0], color=ink, lw=2.7, ls=':', zorder=4)
t = np.linspace(0, 5.5*tau, 700)
u = E * (1-np.exp(-t/tau))
ax.plot(t, u, color=ink, lw=2.7, ls=':', zorder=4)
ax.scatter([0], [0], color=ink, s=30, zorder=6)
# Tangente à droite en zéro : E*t/tau ; elle atteint E au temps tau.
ax.plot([0, 1.12*tau], [0, 1.12*E], color=green,
        lw=1.6, ls=(0, (5, 3)), zorder=5)
ax.scatter([tau], [E], s=45, facecolors='white', edgecolors=green,
           linewidths=1.6, zorder=7)
row = -.22
trans = ax.get_xaxis_transform()
for x, level in [(0, 0), (tau, E)]:
    ax.plot([x, x], [row, (level+.06)/1.28], transform=trans,
            clip_on=False, **guide_style)
ax.annotate('', xy=(0, row), xytext=(tau, row), xycoords=trans,
            arrowprops=dict(arrowstyle='<->', color=green, lw=1.5),
            annotation_clip=False)
ax.text(.5*tau, row-.025, r'$\tau$', transform=trans,
        ha='center', va='top', fontsize=17, color=green)
ax.text(2.1, .40, r'$u(t)=E\left(1-\exp\left(-\frac{t}{\tau}\right)\right)$',
        fontsize=17, color=ink)
fig.legend([Line2D([], [], color=red, lw=4),
            Line2D([], [], color=ink, lw=2.7, ls=':')],
           [r'$e(t)$', r'$u(t)$'],
           loc='lower center', bbox_to_anchor=(.5, .03), ncol=2,
           frameon=False, columnspacing=3)
for label in ax.get_xticklabels():
    label.set_bbox(dict(facecolor='white', edgecolor='none', pad=1))
for ext in ('svg', 'png'):
    fig.savefig(out / f'{Path(__file__).stem}.{ext}', dpi=200,
                bbox_inches='tight', pad_inches=.16, facecolor='white')
plt.close(fig)
