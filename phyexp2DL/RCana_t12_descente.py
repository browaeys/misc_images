#!/usr/bin/env python3
"""Trois figures du temps de demi-descente, exportées au format SVG.

Usage : python RCana_t12_descente.py

Les fichiers sont enregistrés à côté de ce script, indépendamment du dossier
d'où il est exécuté. Dépendances : NumPy et Matplotlib.
Les données sont illustratives, sans lien avec l'acquisition data-normal.txt.
"""

import os
from pathlib import Path
import tempfile

# Un cache temporaire permet aussi l'exécution sur un poste à accès restreint.
os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-rcana-t12")
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


BLEU = "#487bbd"
ROUGE = "#a83f3d"
ORANGE = "#ca8737"
GRIS = "#858b90"
FOND = "#fafbfd"
XMAX = 4.2
U0 = 4.9
U_INF = 0.85
U_DEMI = (U0 + U_INF) / 2
T0 = 0.0

# Échantillonnage régulier d'un signal strictement décroissant.
# Les deux points d'indices 3 et 4 encadrent le seuil de demi-descente.
T_ECHANT = T0 + 0.2 + 0.48 * np.arange(8)
U_ECHANT = np.array([4.6, 4.1, 3.4, 3.1, 2.2, 1.55, 1.16, 1.0])


def cadre():
    """Axes fléchés, fond et typographie communs aux trois figures."""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.subplots_adjust(left=0.12, right=0.96, top=0.96, bottom=0.09)
    ax.set_xlim(-0.03, XMAX + 0.17)
    ax.set_ylim(-0.85, 5.65)
    ax.axis("off")
    ax.add_patch(Rectangle(
        (T0, 0), XMAX, 5.35, facecolor=FOND, edgecolor="#e2e4e7",
        linewidth=1.1, zorder=0,
    ))
    for fin in [(XMAX + 0.13, 0), (T0, 5.62)]:
        ax.annotate(
            "", xy=fin, xytext=(T0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#25292d", lw=1.1,
                            mutation_scale=14, shrinkA=0, shrinkB=0),
        )
    ax.text(XMAX + 0.13, -0.24, "$t$", fontsize=18,
            ha="center", va="top")
    return fig, ax


def niveau(ax, y, label, couleur=GRIS, fin=XMAX):
    ax.plot([T0, fin], [y, y], color=couleur, lw=1.1,
            linestyle=(0, (5, 5)), zorder=1)
    ax.text(-0.12, y, label, ha="right", va="center", fontsize=18,
            clip_on=False)


def projection(ax, t, label, y=U_DEMI, label_y=-0.26):
    ax.plot([t, t], [0, y], color=ROUGE, lw=1.2,
            linestyle=(0, (5, 5)), zorder=2)
    ax.text(t, label_y, label, ha="center", va="top", fontsize=18)


def point_rouge(ax, t):
    ax.scatter([t], [U_DEMI], s=110, color=ROUGE,
               edgecolors="white", linewidths=2, zorder=6)


def figure_continue():
    """Définition sur une courbe continue, monotone et bornée."""
    fig, ax = cadre()
    # Cette forme quelconque décroît strictement sans être une exponentielle
    # simple : le dessin illustre une définition générale de t_{½}.
    a, b = 0.4, 0.32
    t = np.linspace(T0, XMAX - 0.09, 600)
    u = U_INF + (U0 - U_INF) * np.exp(-a * (t - T0) - b * (t - T0)**2)
    t_demi = T0 + (-a + np.sqrt(a**2 + 4 * b * np.log(2))) / (2 * b)
    niveau(ax, U0, "$U_0$")
    niveau(ax, U_INF, "$U_\\infty$")
    niveau(ax, U_DEMI, "$U_{½}$", ROUGE, fin=t_demi)
    ax.plot(t, u, color=BLEU, lw=2.7, solid_capstyle="round", zorder=3)
    projection(ax, t_demi, "$t_{½}$")
    point_rouge(ax, t_demi)
    for bas, haut in [(U_INF, U_DEMI), (U_DEMI, U0)]:
        ax.annotate(
            "", xy=(0.19, bas + 0.04), xytext=(0.19, haut - 0.04),
            arrowprops=dict(arrowstyle="<->", color=GRIS, lw=1,
                            mutation_scale=9),
        )
    ax.text(3.98, U_INF + 0.2, "régime asymptotique", color="#54595e",
            ha="right", va="bottom", fontsize=12)
    ax.text(3.28, U_INF + 0.68, "$u(t)$", fontsize=18)
    ax.text(T0, -0.26, "$t_0$", ha="center", va="top", fontsize=18)
    return fig


def figure_discrete(interpolation=False):
    """Encadrement du seuil : milieu d'intervalle ou interpolation."""
    fig, ax = cadre()
    i = np.flatnonzero(U_ECHANT < U_DEMI)[0] - 1
    ti, tj = T_ECHANT[i:i + 2]
    ui, uj = U_ECHANT[i:i + 2]
    assert ui > U_DEMI > uj
    fraction = (U_DEMI - ui) / (uj - ui)
    t_demi = ti + fraction * (tj - ti) if interpolation else (ti + tj) / 2

    ax.axvspan(ti, tj, ymin=0.85 / 6.5, ymax=6.2 / 6.5,
               color=ORANGE, alpha=0.065, linewidth=0, zorder=1)
    niveau(ax, U_DEMI, "$U_{½}$")
    if interpolation:
        # Seuls les deux points encadrant le seuil sont reliés.
        ax.plot([ti, tj], [ui, uj], color=ORANGE, lw=2.8, zorder=4)
    ax.scatter(T_ECHANT, U_ECHANT, s=66, color=BLEU,
               edgecolors="white", linewidths=1.5, zorder=3)
    ax.scatter([ti, tj], [ui, uj], s=190, facecolors="white",
               edgecolors=ORANGE, linewidths=2.5, zorder=5)
    projection(ax, t_demi, "$t_{½}$", label_y=-0.68)
    point_rouge(ax, t_demi)

    for instant, label in [(ti, "$t_i$"), (tj, "$t_{i+1}$")]:
        ax.text(instant, -0.26, label, ha="center", va="top", fontsize=18)

    fleche = dict(arrowstyle="-", color="#777d83", lw=0.8,
                  connectionstyle="arc3,rad=-0.12", shrinkB=9)
    ax.annotate("point juste avant", xy=(ti, ui), xytext=(0.6, 4.7),
                color="#54595e", fontsize=12, arrowprops=fleche)
    ax.annotate("point juste après", xy=(tj, uj), xytext=(2.82, 1.85),
                color="#54595e", fontsize=12, arrowprops=fleche)

    if interpolation:
        ax.text(t_demi + 0.09, U_DEMI + 0.2, "valeur interpolée",
                color="#54595e", fontsize=12, va="bottom", zorder=7)
    else:
        # Les deux flèches de même longueur montrent le milieu d'intervalle.
        for debut, fin in [(ti, t_demi), (t_demi, tj)]:
            ax.annotate(
                "", xy=(debut + 0.01, 0.32), xytext=(fin - 0.01, 0.32),
                arrowprops=dict(arrowstyle="<->", color=ORANGE,
                                lw=1.1, mutation_scale=9),
            )
        ax.plot([t_demi, t_demi], [0.12, 0.44], color=ORANGE, lw=1.2,
                zorder=5)
    return fig


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "mathtext.fontset": "dejavusans", "mathtext.default": "regular",
        "svg.fonttype": "path",
        "svg.hashsalt": "rcana-demi-descente", "savefig.facecolor": "white",
    })
    dossier = Path(__file__).resolve().parent
    figures = [
        ("RCana_t12_continu", figure_continue()),
        ("RCana_t12_discret1", figure_discrete()),
        ("RCana_t12_discret2", figure_discrete(interpolation=True)),
    ]
    for nom, fig in figures:
        fichier = dossier / f"{nom}.svg"
        fig.savefig(fichier, metadata={"Date": None,
                    "Title": f"Temps de demi-descente — {nom}"})
        plt.close(fig)
        print(fichier)


if __name__ == "__main__":
    main()
