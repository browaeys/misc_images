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
fig, ax = plt.subplots(figsize=(8, 4.9))
fig.subplots_adjust(left=.09, right=.97, bottom=.23, top=.82)
ink, red, grey = '#000000', '#c42b38', '#7d8790'
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
ax.axhline(E, color=grey, lw=.8, ls=(0, (2, 4)), alpha=.6)
ax.plot([0, 0], [0, 1.06], color=grey, lw=1, ls=(0, (2, 4)))
# L'entrée est tracée sous la réponse, y compris sur le palier initial.
ax.plot([-1.3, 0, 0, 5.5], [0, 0, E, E], color=red, lw=4,
        zorder=3, solid_capstyle='butt')
ax.plot([-1.3, 0], [0, 0], color=ink, lw=2.7, ls=':', zorder=4)
t = np.linspace(0, 5.5*tau, 700)
u = E * (1-np.exp(-t/tau))
ax.plot(t, u, color=ink, lw=2.7, ls=':', zorder=4)
ax.scatter([0], [0], color=ink, s=30, zorder=6)
ax.text(2.1, .40, r'$u(t)=E\left(1-\exp\left(-\frac{t}{\tau}\right)\right)$',
        fontsize=17, color=ink)
fig.legend([Line2D([], [], color=ink, lw=2.7, ls=':'),
            Line2D([], [], color=red, lw=4)],
           [r'$u(t)$', r'$e(t)$'],
           loc='lower center', bbox_to_anchor=(.5, .03), ncol=2,
           frameon=False, columnspacing=3)
for ext in ('svg', 'png'):
    fig.savefig(out / f'{Path(__file__).stem}.{ext}', dpi=200,
                bbox_inches='tight', pad_inches=.16, facecolor='white')
plt.close(fig)
