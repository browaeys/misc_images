"""Figure pédagogique ; exécuter avec Python et Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13,
                     'mathtext.fontset': 'dejavusans', 'svg.fonttype': 'none'})
# Temps exprimé en unités de période ; valeurs choisies pour la lisibilité.
U0, A, f, phi = 1.5, 1.0, 1.0, np.pi / 3
T = 1 / f
tm = -phi / (2 * np.pi * f)
t = np.linspace(-0.45, 2.04, 1800)
blue, orange, green, purple = '#2263A5', '#BC5B13', '#227652', '#8045A3'
fig, ax = plt.subplots(figsize=(11, 5.9))
fig.subplots_adjust(left=.20, right=.965, bottom=.08, top=.90)
ax.set(xlim=(-.48, 2.37), ylim=(-.67, 3.18))
ax.axis('off')
ax.annotate('', (2.34, 0), (-.44, 0), arrowprops=dict(arrowstyle='->', lw=1.4, color='#333333'))
ax.annotate('', (0, 3.13), (0, -.12), arrowprops=dict(arrowstyle='->', lw=1.4, color='#333333'))
ax.text(2.34, -.08, '$t$', ha='center', va='top', fontsize=17)
ax.text(-.055, 3.1, '$u(t)$', ha='right', va='center', fontsize=17)
ax.text(.025, -.085, '$0$', va='top')
for y in [U0-A, U0+A]:
    ax.hlines(y, -.42, 2.24, color='#D6D9DD', lw=1, zorder=0)
ax.hlines(U0, -.42, 2.24, color=green, linestyle=(0, (5, 4)), lw=1.25)
for y, label in [(U0+A, '$U_{\max}=U_0+A$'), (U0, '$U_0$'), (U0-A, '$U_{\min}=U_0-A$')]:
    ax.text(-.455, y, label, ha='right', va='center', fontsize=14,
            color=green if y == U0 else '#555555')
ax.plot(t, U0 + A*np.cos(2*np.pi*f*t + phi), lw=2.7, color=blue)
def double_arrow(x1, y1, x2, y2, color):
    ax.annotate('', (x2,y2), (x1,y1), arrowprops=dict(arrowstyle='<->', color=color, lw=1.8, shrinkA=0, shrinkB=0))
# Amplitude du niveau moyen au maximum.
x1, x2 = tm+T, tm+2*T
double_arrow(x1,U0,x1,U0+A,orange)
ax.text(x1+.04, U0+.48*A, '$A$', fontsize=19, color=orange, va='center')
# Amplitude du niveau moyen au minimum.
xmin = tm + 1.5*T
double_arrow(xmin,U0-A,xmin,U0,orange)
ax.text(xmin+.04, U0-.5*A, '$A$', fontsize=19, color=orange, va='center')
# Offset mesuré depuis la tension nulle.
double_arrow(2.16,0,2.16,U0,green)
ax.text(2.2,U0/2,'$U_0$', color=green, fontsize=18, va='center')
# Période entre deux passages montants par le niveau moyen.
period_color = '#008C9E'
p1, p2 = tm + .75*T, tm + 1.75*T
for x in [p1,p2]:
    ax.vlines(x, U0, 2.99, color=period_color, lw=1, linestyles=':')
    ax.plot(x,U0,'o',color=period_color,ms=4)
double_arrow(p1,2.92,p2,2.92,period_color)
ax.text((p1+p2)/2,3.035, r'$T=\dfrac{1}{f}$', color=period_color, ha='center', va='bottom', fontsize=17)
# Phase positive : un maximum précède l'origine.
ax.vlines(tm,-.37,U0+A, color=purple, lw=1, linestyles=(0,(3,3)))
ax.vlines(0,-.37,-.15, color=purple, lw=1, linestyles=(0,(3,3)))
ax.plot(tm,U0+A,'o', color=purple, ms=5)
double_arrow(tm,-.33,0,-.33,purple)
ax.annotate(r'$\Delta t=\dfrac{\varphi}{2\pi f}$', xy=(tm/2,-.33), xytext=(.29,-.42),
            color=purple, fontsize=16, va='center', arrowprops=dict(arrowstyle='-',color=purple,lw=1,connectionstyle='angle,angleA=180,angleB=-90,rad=5'))
out=Path(__file__).resolve().parent
for ext in ('png','svg','pdf'):
    fig.savefig(out/f'signal_sinusoidal.{ext}',dpi=220,facecolor='white',bbox_inches='tight',pad_inches=.2)
print(out/'signal_sinusoidal.png')
