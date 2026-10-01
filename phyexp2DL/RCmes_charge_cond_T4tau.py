"""Générateur en créneaux et réponse RC : période T = 4 tau.

Exécution : python RCmes_charge_cond_T4tau.py (NumPy et Matplotlib requis).
Les figures SVG et PNG sont enregistrées à côté de ce script.
"""
from pathlib import Path
import os

os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib-rcmes')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Paramètres modifiables ; le condensateur est initialement déchargé.
E = 1.0
tau = 1.0
T = 4.0 * tau                 # Période complète ; chaque palier dure T/2.
half_period = T / 2
end = 1.5 * T                 # Trois phases complètes de 2 tau chacune.
out = Path(__file__).resolve().parent

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13})
fig, (ax_e, ax_u) = plt.subplots(2, 1, figsize=(11, 6.2),
                                gridspec_kw={'height_ratios': [1, 1.5]})
fig.subplots_adjust(left=.075, right=.965, top=.93, bottom=.15, hspace=.42)
signal_color, tangent_color, axis_color = '#303438', '#19816b', '#7d8790'


def dimension(ax, a, b, height, label, color):
    """Flèche de durée : abscisses en temps, hauteur relative au graphique."""
    trans = ax.get_xaxis_transform()
    ax.annotate('', xy=(a, height), xytext=(b, height), xycoords=trans,
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.6),
                annotation_clip=False)
    for x in (a, b):
        ax.plot([x, x], [height-.025, height+.025], transform=trans,
                color=color, lw=1.1, clip_on=False)
    ax.text((a+b)/2, height+.035, label, transform=trans,
            ha='center', va='bottom', color=color, fontsize=16)


for ax, label in ((ax_e, r'$e(t)$'), (ax_u, r'$u(t)$')):
    ax.set_xlim(-.1*T, end+.035*T)
    ax.set_ylim(0, 1.27*E)
    ax.set_xticks([])
    ax.set_yticks([0, E], ['0', r'$E$'])
    ax.tick_params(axis='y', length=0, pad=9)
    ax.spines[:].set_visible(False)
    ax.annotate('', xy=(end+.03*T, 0), xytext=(-.1*T, 0),
                arrowprops=dict(arrowstyle='-|>', color=axis_color, lw=1.1),
                annotation_clip=False)
    ax.annotate('', xy=(-.1*T, 1.22*E), xytext=(-.1*T, 0),
                arrowprops=dict(arrowstyle='-|>', color=axis_color, lw=1.1),
                annotation_clip=False)
    ax.text(-.1*T, 1.25*E, label, ha='center', va='bottom', fontsize=17)
    ax.text(end+.03*T, -.06, r'$t$', transform=ax.get_xaxis_transform(),
            ha='right', va='top', fontsize=16)

# Créneaux : les fronts montants sont espacés de T, et non de T/2.
ax_e.plot([-.1*T, 0, 0, half_period, half_period, T, T, end],
          [0, 0, E, E, 0, 0, E, E], color=signal_color, lw=2.5,
          solid_joinstyle='miter', solid_capstyle='butt', clip_on=False)
dimension(ax_e, 0, T, .98, r'$T$', signal_color)

# Solution exacte par morceaux de tau du/dt + u = e(t).
# La tension reste continue aux commutations, sans forcer u à atteindre E ou 0.
ax_u.plot([-.1*T, 0], [0, 0], color=signal_color, lw=2.7, clip_on=False)
u_start = 0.0
phases = []
for n, start in enumerate(np.arange(0, end, half_period)):
    stop = min(start + half_period, end)
    target = E if n % 2 == 0 else 0.0
    phases.append((start, u_start, target))
    t = np.linspace(start, stop, 500)
    u = target + (u_start - target) * np.exp(-(t-start)/tau)
    ax_u.plot(t, u, color=signal_color, lw=2.7, zorder=4, clip_on=False)
    u_start = u[-1]

# Asymptote u = E sur toute la largeur du tracé.
ax_u.axhline(E, color=axis_color, lw=1, ls=(0, (3, 3)), zorder=1)

# À chaque commutation, la tangente rejoint le niveau cible après tau,
# même si le condensateur n'a pas tout à fait atteint le palier précédent.
row = -.23
for start, initial, target in phases:
    duration = 1.12*tau if target == E else tau
    tangent_end = initial + (target-initial)*duration/tau
    ax_u.plot([start, start+duration], [initial, tangent_end],
              color=tangent_color, lw=1.4, ls=(0, (5, 3)), zorder=5)
    ax_u.scatter([start+tau], [target], s=40, facecolors='white',
                 edgecolors=tangent_color, linewidths=1.6,
                 zorder=6, clip_on=False)
    for x, y in ((start, initial), (start+tau, target)):
        ax_u.plot([x, x], [row, y/(1.27*E)],
                  transform=ax_u.get_xaxis_transform(), color=tangent_color,
                  lw=1, ls=(0, (3, 3)), clip_on=False)
    dimension(ax_u, start, start+tau, row, r'$\tau$', tangent_color)

for ext in ('svg', 'png'):
    fig.savefig(out / f'{Path(__file__).stem}.{ext}', dpi=200,
                bbox_inches='tight', pad_inches=.12, facecolor='white')
plt.close(fig)
