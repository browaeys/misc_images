"""Échelon de tension et réponse RC, en charge et en décharge."""
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
fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
fig.subplots_adjust(left=.065, right=.975, bottom=.32, top=.84, wspace=.22)
ink, red, grey = '#000000', '#c42b38', '#7d8790'
green = '#19816b'
guide_style = dict(color='#b7bec4', lw=.9, ls=(0, (2, 4)))
t0, tau = 0., 1.
for ax, B, C, title in zip(axes, [.25, 1.], [1., .25],
                         ['Charge : $C>B$', 'Décharge : $C<B$']):
    ax.set_xlim(-1.3, 5.7)
    ax.set_ylim(0, 1.22)
    ax.spines[:].set_visible(False)
    ax.set_xticks([t0], [r'$t_0$'])
    ax.set_yticks([B, C], [r'$B$', r'$C$'])
    ax.tick_params(length=0, pad=9)
    ax.set_title(title, fontsize=17, pad=23, color=ink)
    for end in [(5.7, 0), (-1.3, 1.2)]:
        ax.annotate('', xy=end, xytext=(-1.3, 0),
                    arrowprops=dict(arrowstyle='-|>', color=grey, lw=1.1),
                    annotation_clip=False)
    ax.text(5.7, -.045, r'$t$', ha='right', va='top', fontsize=17)
    ax.text(-1.3, 1.23, 'Tension', ha='left', fontsize=13, color=ink)
    for level in [B, C]:
        ax.axhline(level, **guide_style)
    ax.plot([t0, t0], [0, 1.06], **guide_style)
    # La réponse continue se superpose à l'entrée avant l'échelon.
    ax.plot([-1.3, t0], [B, B], color=ink, lw=2.7, ls=':', zorder=4)
    t = np.linspace(t0, 5.5, 700)
    u = C + (B-C)*np.exp(-(t-t0)/tau)
    ax.plot(t, u, color=ink, lw=2.7, ls=':', zorder=4)
    ax.plot([-1.3, t0, t0, 5.5], [B, B, C, C], color=red,
            lw=4, zorder=3)
    ax.scatter([t0], [B], color=ink, s=30, zorder=6)
    # Tangente à droite en t0 : B + (C-B)(t-t0)/tau.
    ax.plot([t0, t0+1.12*tau], [B, B+1.12*(C-B)],
            color=green, lw=1.6, ls=(0, (5, 3)), zorder=5)
    ax.scatter([t0+tau], [C], s=45, facecolors='white',
               edgecolors=green, linewidths=1.6, zorder=7)
    row = -.22
    trans = ax.get_xaxis_transform()
    for x, level in [(t0, B), (t0+tau, C)]:
        ax.plot([x, x], [row, level/1.22], transform=trans,
                clip_on=False, **guide_style)
    ax.annotate('', xy=(t0, row), xytext=(t0+tau, row), xycoords=trans,
                arrowprops=dict(arrowstyle='<->', color=green, lw=1.5),
                annotation_clip=False)
    ax.text(t0+.5*tau, row-.025, r'$\tau$', transform=trans,
            ha='center', va='top', fontsize=17, color=green)
    for label in ax.get_xticklabels():
        label.set_bbox(dict(facecolor='white', edgecolor='none', pad=1))
    # L'annotation souligne la continuité sans masquer les courbes.
    ax.annotate(r'$u(t_0)=B$', xy=(t0, B),
                xytext=(1.15, .12 if C>B else 1.13),
                color=ink, fontsize=13, ha='center',
                bbox=dict(facecolor='white', edgecolor='none', pad=1),
                arrowprops=dict(arrowstyle='-', lw=.9, color=grey))

fig.legend([Line2D([], [], color=red, lw=4),
            Line2D([], [], color=ink, lw=2.7, ls=':')],
           [r'$e(t)$', r'$u(t)$'],
           loc='lower center', bbox_to_anchor=(.5, .03), ncol=2,
           frameon=False, columnspacing=3)
for ext in ('svg', 'png'):
    fig.savefig(out / f'{Path(__file__).stem}.{ext}', dpi=200,
                bbox_inches='tight', pad_inches=.16, facecolor='white')
plt.close(fig)
