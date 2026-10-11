#!/usr/bin/env python3
"""Illustrer l'encadrement du temps de demi-descente d'un signal bruité.

Usage : python RCana_t12_bruit.py
Dépendances : NumPy et Matplotlib. Sortie : RCana_t12_bruit.svg, à côté
du script. Les données sont simulées pour illustrer plusieurs franchissements
du seuil ; elles ne proviennent pas de data-normal.txt.
"""

import os
from pathlib import Path
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-rcana-t12")
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox
import numpy as np


BLEU = "#487bbd"
ORANGE = "#ca8737"
GRIS = "#858b90"
U0, U_INF, TAU = 4.9, 0.85, 1.8
U_DEMI = (U0 + U_INF) / 2
XMAX = 4.2


def modele(t):
    return U_INF + (U0 - U_INF) * np.exp(-t / TAU)


def donnees_et_bornes():
    # Assez de points pour montrer le bruit, avec un pas visible sur le schéma.
    t = np.linspace(0, 4.1, 80)
    rng = np.random.default_rng(23)
    u = modele(t) + rng.uniform(-0.45, 0.45, len(t))
    # Choix des bornes utilisé dans le notebook : un échantillon de marge
    # autour du premier passage sous le seuil et du dernier point au-dessus.
    premier_sous = np.flatnonzero(u < U_DEMI)[0]
    dernier_dessus = np.flatnonzero(u > U_DEMI)[-1]
    # Écarter légèrement ce point du seuil pour faciliter la lecture du dessin.
    u[dernier_dessus] += 0.08
    if premier_sous == 0 or dernier_dessus == len(t) - 1:
        raise ValueError("L'acquisition doit encadrer les franchissements.")
    i_min = premier_sous - 1
    i_max = dernier_dessus + 1
    return t, u, i_min, i_max


def figure():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "mathtext.fontset": "dejavusans", "mathtext.default": "regular",
        "svg.fonttype": "path", "svg.hashsalt": "rcana-demi-descente-bruit",
        "savefig.facecolor": "white",
    })
    t, u, i_min, i_max = donnees_et_bornes()
    t_min, t_max = t[i_min], t[i_max]
    premier_sous = i_min + 1
    dernier_dessus = i_max - 1

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.subplots_adjust(left=0.12, right=0.96, top=0.96, bottom=0.09)
    ax.set_xlim(-0.03, XMAX + 0.17)
    ax.set_ylim(-0.85, 5.65)
    ax.axis("off")
    ax.add_patch(Rectangle(
        (0, 0), XMAX, 5.35, facecolor="#fafbfd", edgecolor="#e2e4e7",
        linewidth=1.1, zorder=0,
    ))
    ax.add_patch(Rectangle(
        (t_min, 0), t_max - t_min, 5.35,
        facecolor=ORANGE, alpha=0.10, edgecolor="none", zorder=1,
    ))
    for fin in [(XMAX + 0.13, 0), (0, 5.62)]:
        ax.annotate(
            "", xy=fin, xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color="#25292d", lw=1.1,
                            mutation_scale=14, shrinkA=0, shrinkB=0),
        )
    ax.text(XMAX + 0.13, -0.24, "$t$", fontsize=18, ha="center", va="top")
    ax.text(0, -0.26, "0", fontsize=18, ha="center", va="top")

    ax.plot([0, XMAX], [U_DEMI, U_DEMI], color=GRIS,
            lw=1.2, linestyle=(0, (5, 5)), zorder=2)
    ax.text(-0.12, U_DEMI, "$U_{½}$", ha="right", va="center",
            fontsize=18, clip_on=False)
    ax.scatter(t, u, s=24, color=BLEU, edgecolors="white", linewidths=0.5,
               zorder=4)

    # Les points entourés sont les franchissements extrêmes ; les bornes
    # correspondent aux échantillons voisins situés juste à l'extérieur.
    for indice in [premier_sous, dernier_dessus]:
        ax.scatter([t[indice]], [u[indice]], s=110, facecolors="none",
                   edgecolors=ORANGE, linewidths=2, zorder=5)
        ax.plot([t[indice], t[indice]], [0, u[indice]], color=GRIS,
                lw=0.8, linestyle=(0, (2, 4)), zorder=2)

    voisins = (t >= t_min - 0.08) & (t <= t_max + 0.08)
    ax.vlines(t[voisins], -0.08, 0, color=GRIS, linewidth=0.7, zorder=3)
    for instant, label in [
        (t_min, "$t_{½}^{min}$"),
        (t_max, "$t_{½}^{max}$"),
    ]:
        ax.plot([instant, instant], [0, 5.35], color=ORANGE, lw=1.2,
                linestyle=(0, (4, 4)), zorder=2)
        ax.plot([instant, instant], [-0.09, 0.09], color=ORANGE, lw=1.5,
                zorder=3)
        ax.text(instant, -0.26, label, ha="center", va="top", fontsize=18)

    fleche = dict(arrowstyle="-", color=GRIS, lw=0.9,
                  connectionstyle="arc3,rad=-0.12", shrinkB=8)
    ax.annotate("Premier point\nsous le seuil",
                xy=(t[premier_sous], u[premier_sous]), xytext=(0.08, 2.3),
                fontsize=11, color="#54595e", va="center",
                arrowprops=fleche)
    ax.annotate("Dernier point\nau-dessus du seuil",
                xy=(t[dernier_dessus], u[dernier_dessus]),
                xytext=(2.02, 4.48), fontsize=11, color="#54595e",
                va="center", arrowprops=fleche)

    ax.text(t_min / 2, U_DEMI + 0.10, "$u > U_{½}$", fontsize=16,
            color=BLEU, ha="center", va="bottom")
    ax.text((t_max + XMAX) / 2, U_DEMI - 0.10, "$u < U_{½}$", fontsize=16,
            color=BLEU, ha="center", va="top")

    ax.annotate(
        "", xy=(t_min, 0.42), xytext=(t_max, 0.42),
        arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.5,
                        mutation_scale=12, shrinkA=0, shrinkB=0),
    )
    ax.text((t_min + t_max) / 2, 0.64, "Encadrement",
            fontsize=11, color="#98601e", ha="center", va="bottom")
    return fig


def bounding_box_serree(fig):
    """Encadrer les éléments dessinés, sans les marges des axes invisibles."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    # Les points du signal sont à l'intérieur du rectangle de fond : ses
    # limites couvrent donc aussi les marqueurs. Les textes et les flèches
    # peuvent dépasser ce rectangle et sont pris en compte séparément.
    elements = [element for ax in fig.axes
                for element in [*ax.texts, *ax.lines, *ax.patches]
                if element.get_visible()]
    boite = Bbox.union([element.get_window_extent(renderer)
                        for element in elements])
    boite = boite.transformed(fig.dpi_scale_trans.inverted())
    # Un point de marge protège les contours des flèches et des traits.
    marge = 1 / 72
    return Bbox.from_extents(boite.x0 - marge, boite.y0 - marge,
                             boite.x1 + marge, boite.y1 + marge)


def main():
    fig = figure()
    fichier = Path(__file__).resolve().with_suffix(".svg")
    fig.savefig(fichier, bbox_inches=bounding_box_serree(fig), pad_inches=0,
                metadata={
        "Date": None, "Title": "Encadrement du temps de demi-descente",
        "Description": "Signal bruité : le premier point sous le seuil et "
        "le dernier point au-dessus sont entourés. La borne minimale est "
        "l'instant échantillonné juste avant le premier, et la borne maximale "
        "l'instant échantillonné juste après le dernier.",
    })
    plt.close(fig)
    print(fichier)


if __name__ == "__main__":
    main()
