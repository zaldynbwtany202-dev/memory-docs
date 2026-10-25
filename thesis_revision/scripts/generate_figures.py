#!/usr/bin/env python3
"""Generate original, source-independent pedagogical diagrams for the revision."""
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch, FancyBboxPatch, Arc
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
BLUE = "#1f4e79"
TEAL = "#2a7f8e"
LIGHT = "#e8f1f5"
SAND = "#e7d4a5"
CLAY = "#c6a68c"
ROCK = "#9b9b96"
WATER = "#bfe3f2"
ORANGE = "#d97925"
RED = "#a23b3b"
GREEN = "#4b7d58"
DARK = "#263238"


def canvas(name, width=9, height=5.2):
    fig, ax = plt.subplots(figsize=(width, height), dpi=180)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax, OUT / f"{name}.png"


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.12, facecolor="white")
    plt.close(fig)


def box(ax, x, y, w, h, text, color=BLUE, fontsize=9, fill=LIGHT):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
                           linewidth=1.2, edgecolor=color, facecolor=fill)
    ax.add_patch(patch)
    max_chars = max(8, int(w * 1.15 * (9 / fontsize)))
    wrapped = []
    for explicit_line in text.split("\n"):
        wrapped.extend(textwrap.wrap(explicit_line, max_chars) or [""])
    ax.text(x+w/2, y+h/2, "\n".join(wrapped),
            ha="center", va="center", fontsize=fontsize, color=DARK, linespacing=1.25)
    return patch


def arrow(ax, x1, y1, x2, y2, color=BLUE, style="-|>", lw=1.4, rad=0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                mutation_scale=12, linewidth=lw, color=color,
                                connectionstyle=f"arc3,rad={rad}"))


def title(ax, text):
    ax.text(50, 97, text, ha="center", va="top", fontsize=13, weight="bold", color=BLUE)


def history():
    fig, ax, path = canvas("history_timeline", 10, 4.8)
    title(ax, "Du principe porteur à la gestion du cycle de vie")
    ax.plot([7, 94], [48, 48], color=BLUE, lw=2)
    events = [
        (9, "Antiquité", "Arches et piles\nen maçonnerie"),
        (24, "1779", "Iron Bridge :\narc en fonte"),
        (39, "1883", "Brooklyn Bridge :\nsuspension par câbles d’acier"),
        (55, "XXe siècle", "Béton armé puis\nbéton précontraint"),
        (70, "1956", "Strömsund :\njalon des ponts haubanés modernes"),
        (87, "Époque actuelle", "Durabilité, inspection,\nmonitoring et cycle de vie"),
    ]
    for i, (x, date, label) in enumerate(events):
        ax.add_patch(Circle((x, 48), 1.6, color=ORANGE, zorder=3))
        above = i % 2 == 0
        y0, y1 = (52, 75) if above else (26, 44)
        ax.plot([x, x], [48, y0 if above else 44], color=TEAL, lw=1)
        ax.text(x, y1 if above else 20, date, ha="center", va="center", fontsize=10, weight="bold", color=BLUE)
        ax.text(x, 65 if above else 31, label, ha="center", va="center", fontsize=8.5, color=DARK)
    ax.text(50, 4, "L’évolution des portées s’accompagne d’une exigence croissante sur les appuis, le lit et le modèle géotechnique.",
            ha="center", fontsize=9, style="italic", color=DARK)
    save(fig, path)


def four_families():
    fig, ax, path = canvas("four_bridge_families", 10, 6.2)
    title(ax, "Quatre familles structurales et chemins de transmission des charges")
    panels = [(3, 52, "A. Poutres et dalles"), (52, 52, "B. Arcs"), (3, 5, "C. Suspendus"), (52, 5, "D. Haubanés")]
    for x, y, lab in panels:
        ax.add_patch(Rectangle((x, y), 45, 38, fill=False, edgecolor="#b0bec5", lw=1))
        ax.text(x+2, y+35, lab, fontsize=10.5, weight="bold", color=BLUE, va="top")
    # Beam
    ax.plot([8, 43], [70, 70], color=DARK, lw=5)
    for x in [10, 41]:
        ax.plot([x, x], [70, 59], color=DARK, lw=3)
        ax.add_patch(Rectangle((x-3, 56), 6, 3, facecolor=ROCK, edgecolor=DARK))
    for x in [18, 26, 34]:
        arrow(ax, x, 83, x, 73, ORANGE)
    arrow(ax, 12, 67, 10, 60, TEAL); arrow(ax, 39, 67, 41, 60, TEAL)
    ax.text(26, 58, "flexion • réactions aux appuis", ha="center", fontsize=8)
    # Arch
    ax.add_patch(Arc((75, 60), 32, 27, theta1=0, theta2=180, lw=5, color=DARK))
    ax.plot([59, 91], [60, 60], color=DARK, lw=2)
    for x in [61, 89]:
        ax.add_patch(Rectangle((x-3, 53), 6, 6, facecolor=ROCK, edgecolor=DARK))
        arrow(ax, 75 if x == 61 else 75, 60, x, 56, TEAL)
    for x in [67, 75, 83]: arrow(ax, x, 84, x, 75, ORANGE)
    ax.text(75, 65, "compression\npoussées horizontales", ha="center", fontsize=8)
    # Suspension
    xs = np.linspace(11, 40, 100)
    ys = 27 + 0.038*(xs-25.5)**2
    ax.plot(xs, ys, color=BLUE, lw=2)
    for x in [11, 40]: ax.plot([x, x], [15, 35], color=DARK, lw=3)
    ax.plot([8, 43], [21, 21], color=DARK, lw=4)
    for x in np.linspace(12, 39, 8):
        y = 27 + 0.038*(x-25.5)**2
        ax.plot([x, x], [21, y], color=TEAL, lw=0.8)
    arrow(ax, 25, 26, 25, 23, ORANGE)
    ax.text(26, 10, "câbles en traction • ancrages et pylônes", ha="center", fontsize=8)
    # Cable stayed
    ax.plot([57, 94], [21, 21], color=DARK, lw=4)
    for x in [64, 86]:
        ax.plot([x, x], [15, 35], color=DARK, lw=3)
        for xx in [57, 72, 78, 94]:
            if (x == 64 and xx <= 78) or (x == 86 and xx >= 72):
                ax.plot([x, xx], [33, 21], color=BLUE, lw=1)
    for x in [60, 73, 91]: arrow(ax, x, 32, x, 23, ORANGE)
    ax.text(75, 10, "haubans inclinés • flexion du tablier et compression des pylônes", ha="center", fontsize=7.7)
    save(fig, path)


def components():
    fig, ax, path = canvas("bridge_components")
    title(ax, "Chaîne fonctionnelle d’un pont et de ses fondations")
    ax.add_patch(Rectangle((0, 42), 100, 25, facecolor=SAND, edgecolor="none"))
    ax.add_patch(Rectangle((0, 30), 100, 12, facecolor=CLAY, edgecolor="none"))
    ax.add_patch(Rectangle((0, 12), 100, 18, facecolor=ROCK, edgecolor="none"))
    ax.add_patch(Rectangle((0, 62), 100, 12, facecolor=WATER, edgecolor="none"))
    ax.plot([5, 95], [79, 79], color=DARK, lw=6)
    ax.text(50, 84, "Tablier et chaussée", ha="center", fontsize=10, weight="bold")
    for x in [15, 50, 85]:
        ax.add_patch(Rectangle((x-2, 61), 4, 18, facecolor="#777777", edgecolor=DARK))
        ax.add_patch(Rectangle((x-6, 55), 12, 6, facecolor="#aaaaaa", edgecolor=DARK))
        ax.add_patch(Rectangle((x-4, 42), 8, 13, facecolor="#888888", edgecolor=DARK))
    ax.text(50, 68, "Pile", ha="center", color="white", fontsize=9, weight="bold")
    ax.text(15, 68, "Culée", ha="center", color="white", fontsize=9, weight="bold")
    ax.text(85, 50, "Semelle / tête de pieux", ha="center", fontsize=8)
    for x in [48, 52]: ax.plot([x, x], [42, 20], color=DARK, lw=2)
    ax.text(58, 29, "Fondation\nprofonde", fontsize=8, va="center")
    ax.text(23, 48, "Horizon compressible", fontsize=8)
    ax.text(25, 20, "Substratum : portance et déformabilité à vérifier", fontsize=8, color="white")
    ax.text(72, 69, "Niveau d’eau / hydraulique", fontsize=8, color=BLUE)
    arrow(ax, 90, 90, 90, 82, ORANGE); ax.text(87, 89, "Actions", ha="right", fontsize=9, color=ORANGE)
    save(fig, path)


def foundation_alternatives():
    fig, ax, path = canvas("foundation_alternatives", 10, 5.6)
    title(ax, "Alternatives de fondation : le choix dépend du modèle de sol et des sollicitations")
    ax.add_patch(Rectangle((0, 25), 100, 24, facecolor=SAND, edgecolor="none"))
    ax.add_patch(Rectangle((0, 10), 100, 15, facecolor=ROCK, edgecolor="none"))
    ax.text(20, 17, "Horizon résistant\nPosition et variabilité à démontrer", ha="center", fontsize=9, color="white")
    ax.text(20, 39, "Formations superficielles\nRésistance, compressibilité, eau, érodabilité", ha="center", fontsize=9)
    for x, lab in [(20, "Semelle superficielle"), (50, "Pieux / barrettes"), (80, "Puits ou caisson")]:
        ax.add_patch(Rectangle((x-11, 69), 22, 6, facecolor="#888888", edgecolor=DARK))
        ax.text(x, 83, lab, ha="center", fontsize=10, weight="bold", color=BLUE)
    ax.add_patch(Rectangle((10, 49), 20, 8, facecolor="#999999", edgecolor=DARK))
    for x in [45, 50, 55]: ax.plot([x, x], [69, 20], color=DARK, lw=2.5)
    ax.add_patch(Rectangle((75, 28), 10, 41, facecolor="#999999", edgecolor=DARK))
    ax.text(20, 58, "Vérifier portance,\ntassements et affouillement", ha="center", fontsize=8)
    ax.text(50, 58, "Transfert en pointe +\nfrottement latéral", ha="center", fontsize=8, bbox=dict(facecolor="white", alpha=.7, edgecolor="none"))
    ax.text(80, 58, "Constructibilité,\ncontrôle du fond et de l’eau", ha="center", fontsize=8, bbox=dict(facecolor="white", alpha=.7, edgecolor="none"))
    ax.text(50, 3, "Aucune alternative n’est déduite de la seule portée du pont.", ha="center", fontsize=9, style="italic")
    save(fig, path)


def load_path():
    fig, ax, path = canvas("load_path", 9, 4.8)
    title(ax, "Sollicitations et rétroactions sol–fondation–structure")
    labels = ["Actions\n(permanentes, trafic, eau, vent, séisme)", "Tablier et\nappareils d’appui", "Piles, culées\net remblais", "Fondations", "Terrain et\nhydrogéologie"]
    xs = [2, 22, 42, 62, 82]
    for x, lab in zip(xs, labels): box(ax, x, 48, 16, 23, lab, fontsize=8.3)
    for x in xs[:-1]: arrow(ax, x+16, 59, x+20, 59)
    arrow(ax, 90, 43, 10, 43, TEAL, rad=-0.20)
    ax.text(50, 24, "Déplacements, rotations, variations de pression interstitielle et changements de rigidité modifient la répartition des effets.",
            ha="center", fontsize=9, color=DARK)
    ax.text(50, 12, "La reconnaissance doit donc fournir des paramètres de résistance ET de déformation, avec leur incertitude.",
            ha="center", fontsize=9, weight="bold", color=BLUE)
    save(fig, path)


def valley():
    fig, ax, path = canvas("valley_ground_model", 9, 5.4)
    title(ax, "Modèle conceptuel d’une vallée alluviale")
    xs = np.array([0, 15, 28, 42, 58, 72, 85, 100])
    surface = np.array([77, 73, 68, 63, 62, 66, 72, 79])
    rock = np.array([50, 44, 34, 25, 22, 28, 39, 52])
    ax.fill_between(xs, rock, surface, color=SAND, alpha=.95, label="Alluvions et terrasses")
    ax.fill_between(xs, 0, rock, color=ROCK, alpha=.95, label="Substratum")
    ax.fill_between([30, 70], [58, 58], [63, 63], color=WATER)
    ax.plot(xs, surface, color=DARK, lw=1.4)
    ax.plot(xs, rock, color=DARK, lw=1.2)
    ax.plot([0, 100], [58, 58], color=TEAL, lw=1.2, ls="--")
    ax.text(8, 64, "Nappe : niveau et variations à mesurer", fontsize=8.5, color=BLUE,
            bbox=dict(facecolor=SAND, alpha=.85, edgecolor="none", pad=.6))
    ax.text(8, 70, "Terrasse : géométrie et faciès variables", fontsize=8.5,
            bbox=dict(facecolor=SAND, alpha=.85, edgecolor="none", pad=.6))
    ax.text(61, 42, "Chenal actif : mobilité du lit et affouillement", fontsize=8.5, ha="center")
    ax.text(60, 14, "Substratum : fracturation, altération et cavités éventuelles", fontsize=8.5, ha="center", color="white")
    for x in [22, 78]:
        ax.plot([x, x], [surface[np.argmin(abs(xs-x))], rock[np.argmin(abs(xs-x))]-5], color=DARK, lw=3)
        ax.text(x, 86, "Appui", ha="center", fontsize=9, weight="bold")
    save(fig, path)


def workflow():
    fig, ax, path = canvas("investigation_workflow", 10, 5.4)
    title(ax, "Programme de reconnaissance adaptatif et traçable")
    steps = [
        (4, 61, "1. Données existantes\nGéologie, historique du lit, ouvrages, risques"),
        (28, 61, "2. Visite et modèle initial\nAccès, faciès, appuis, eau, indices de désordres"),
        (52, 61, "3. Investigations initiales\nSondages, essais et géophysique choisis par objectif"),
        (76, 61, "4. Modèle géotechnique\nCouches, paramètres, eau, incertitudes"),
        (18, 19, "5. Lacunes critiques ?\nAnomalies ou hypothèses gouvernant le projet"),
        (56, 19, "6. Investigations ciblées\nVérifier, densifier ou instrumenter si nécessaire"),
    ]
    for x, y, text in steps: box(ax, x, y, 20, 20, text, fontsize=8.2)
    arrow(ax, 24, 71, 28, 71); arrow(ax, 48, 71, 52, 71); arrow(ax, 72, 71, 76, 71)
    arrow(ax, 86, 61, 38, 40, TEAL); arrow(ax, 38, 29, 56, 29, TEAL)
    arrow(ax, 66, 40, 86, 61, GREEN, rad=-.15)
    ax.text(50, 7, "Le nombre et la profondeur des investigations sont des résultats du raisonnement, non des valeurs universelles fixées à l’avance.",
            ha="center", fontsize=9, weight="bold", color=BLUE)
    save(fig, path)


def tests():
    fig, ax, path = canvas("insitu_tests", 10, 5.6)
    title(ax, "Trois essais in situ : mesures différentes, interprétations non interchangeables")
    for x, lab in [(4, "SPT"), (37, "CPT / CPTu"), (70, "Pressiomètre Ménard")]:
        ax.add_patch(Rectangle((x, 10), 26, 75, facecolor="#fafafa", edgecolor="#b0bec5"))
        ax.text(x+13, 80, lab, ha="center", fontsize=11, weight="bold", color=BLUE)
    # SPT
    ax.add_patch(Rectangle((11, 62), 12, 5, facecolor=ORANGE, edgecolor=DARK))
    arrow(ax, 17, 61, 17, 49, ORANGE)
    ax.plot([17, 17], [49, 25], color=DARK, lw=2)
    ax.add_patch(Rectangle((14, 22), 6, 6, facecolor=ROCK, edgecolor=DARK))
    ax.text(17, 16, "N et échantillon remanié\nDocumenter énergie et forage", ha="center", fontsize=8)
    # CPT
    ax.plot([50, 50], [66, 32], color=DARK, lw=2)
    ax.add_patch(Polygon([[47, 32], [53, 32], [50, 25]], facecolor=TEAL, edgecolor=DARK))
    ax.add_patch(Rectangle((47, 39), 6, 7, facecolor=LIGHT, edgecolor=DARK))
    arrow(ax, 50, 72, 50, 64, ORANGE)
    ax.text(50, 16, "qc, fs ; u2 et dissipation en CPTu\nProfil continu, sans échantillon", ha="center", fontsize=8)
    # PMT
    ax.plot([83, 83], [68, 32], color=DARK, lw=2)
    ax.add_patch(FancyBboxPatch((79, 30), 8, 24, boxstyle="round,pad=.2", facecolor=LIGHT, edgecolor=BLUE))
    for y in [36, 42, 48]: arrow(ax, 83, y, 90, y, TEAL); arrow(ax, 83, y, 76, y, TEAL)
    ax.text(83, 16, "Courbe pression–volume\nEM et pression limite\nselon protocole", ha="center", fontsize=8)
    save(fig, path)


def geophysics():
    fig, ax, path = canvas("geophysics_calibration", 9, 5.4)
    title(ax, "La géophysique guide les vérifications ; elle ne prouve pas, à elle seule, une cavité")
    ax.add_patch(Rectangle((0, 12), 100, 44, facecolor=SAND, edgecolor="none"))
    ax.add_patch(Rectangle((0, 0), 100, 12, facecolor=ROCK, edgecolor="none"))
    ax.add_patch(Circle((66, 27), 8, facecolor="white", edgecolor=RED, lw=1.5, ls="--"))
    ax.text(66, 27, "Anomalie\nà expliquer", ha="center", fontsize=8, color=RED)
    ax.plot([5, 95], [62, 62], color=DARK, lw=1.5)
    for x in np.linspace(10, 90, 9):
        ax.add_patch(Circle((x, 62), 1, color=BLUE))
        if x < 85: ax.plot([x, x+10], [62, 52], color=TEAL, lw=.6, alpha=.6)
    ax.text(24, 72, "ERT : contrastes de résistivité", fontsize=9, color=BLUE)
    ax.text(24, 67, "GPR : réflexions électromagnétiques", fontsize=9, color=BLUE)
    ax.text(24, 57, "Sismique : propagation des ondes", fontsize=9, color=BLUE)
    ax.plot([66, 66], [62, 14], color=DARK, lw=2, ls="--")
    ax.add_patch(Rectangle((61, 62), 10, 5, facecolor=ORANGE, edgecolor=DARK))
    ax.text(73, 47, "Sondage de contrôle\net essais ciblés", fontsize=9, color=DARK)
    ax.text(50, 5, "Géométrie, eau, argiles, hétérogénéité et ouvrages enterrés peuvent produire des signatures ambiguës.", ha="center", fontsize=9)
    save(fig, path)


def risks():
    fig, ax, path = canvas("risk_interactions", 8, 6)
    title(ax, "Les risques se combinent au niveau d’un appui")
    box(ax, 34, 39, 32, 22, "Appui + fondation\nPerformance, sécurité et durabilité", fontsize=10, fill="#fff4e6", color=ORANGE)
    items = [
        (5, 68, "Hydrologie / hydraulique\nCrue, contraction, affouillement"),
        (67, 68, "Terrain\nHétérogénéité,\ncompressibilité, karst"),
        (3, 14, "Séisme\nLiquéfaction, déplacements, interaction"),
        (67, 14, "Eau et matériaux\nAgressivité, drainage, durabilité"),
    ]
    for x, y, text in items: box(ax, x, y, 30, 17, text, fontsize=8.2)
    arrow(ax, 27, 68, 42, 61); arrow(ax, 74, 68, 58, 61)
    arrow(ax, 27, 31, 42, 39); arrow(ax, 74, 31, 58, 39)
    ax.text(50, 5, "L’érosion interne, l’instabilité de rive, l’exécution et l’entretien complètent ce système.", ha="center", fontsize=9)
    save(fig, path)


def scour():
    fig, ax, path = canvas("scour_components", 9, 5.4)
    title(ax, "Décomposition physique de l’abaissement du lit")
    x = np.linspace(0, 100, 200)
    initial = 55 + 3*np.sin(x/13)
    final = initial - 3 - 6*np.exp(-((x-52)/22)**2) - 10*np.exp(-((x-50)/7)**2)
    ax.fill_between(x, 0, final, color=SAND)
    ax.fill_between(x, final, initial, color=WATER, alpha=.9)
    ax.plot(x, initial, color=DARK, lw=1.2, ls="--", label="Lit initial")
    ax.plot(x, final, color=BLUE, lw=2, label="Lit après évolution")
    ax.add_patch(Rectangle((47, 51), 6, 30, facecolor="#777777", edgecolor=DARK))
    ax.text(50, 85, "Pile", ha="center", fontsize=9, weight="bold")
    ax.text(16, 65, "Dégradation à long terme", fontsize=9, color=BLUE)
    arrow(ax, 20, 62, 20, 55, BLUE)
    ax.text(70, 65, "Contraction de l’écoulement", fontsize=9, color=BLUE)
    arrow(ax, 72, 61, 66, 49, BLUE)
    ax.text(50, 26, "Affouillement local\nautour de l’obstacle", ha="center", fontsize=9, color=RED)
    ax.text(50, 12, "Abaissement de calcul = dégradation + contraction + affouillement local\n(selon les hypothèses et combinaisons du référentiel retenu)", ha="center", fontsize=9, weight="bold")
    save(fig, path)


def erosion():
    fig, ax, path = canvas("internal_erosion_mechanisms", 9, 5.2)
    title(ax, "Quatre mécanismes d’érosion interne à distinguer")
    items = [
        (4, 54, "Renard régressif", "Progression d’un conduit depuis un exutoire sous gradient et conditions favorables."),
        (52, 54, "Suffusion", "Migration sélective des fines à travers le squelette granulaire, sans formation nécessaire d’un conduit."),
        (4, 12, "Érosion de contact", "Entraînement à l’interface de couches dont les granulométries sont incompatibles."),
        (52, 12, "Fuite concentrée", "Érosion le long d’une fissure, d’un interface ou d’un élément enterré."),
    ]
    for x, y, head, body in items:
        box(ax, x, y, 44, 25, head+"\n"+body, fontsize=8.5)
    ax.text(50, 5, "Diagnostic : géométrie + granulométrie + écoulement + preuves de transport ; le gradient seul ne suffit pas.", ha="center", fontsize=9, weight="bold", color=BLUE)
    save(fig, path)


def liquefaction():
    fig, ax, path = canvas("liquefaction_chain", 10, 5)
    title(ax, "Chaîne d’évaluation de la liquéfaction et de ses conséquences")
    labels = [
        (2, "Susceptibilité du sol\nGranulométrie, état, histoire"),
        (22, "Eau souterraine\nNiveau et variations"),
        (42, "Sollicitation sismique\nAccélération, durée\net fréquences"),
        (62, "Réponse du sol\nCSR / résistance et pressions interstitielles"),
        (82, "Conséquences\nDéformations, portance, interaction"),
    ]
    for x, text in labels: box(ax, x, 48, 16, 23, text, fontsize=8)
    for x in [2, 22, 42, 62]: arrow(ax, x+16, 59, x+20, 59)
    ax.text(50, 32, "Le dépistage SPT, CPT ou Vs est un maillon ; il ne remplace ni le modèle de site ni l’évaluation des déplacements.", ha="center", fontsize=9)
    ax.text(50, 17, "Les seuils de N, qc ou Vs ne sont pas des interrupteurs universels : corrections, magnitude et domaine de validité sont indispensables.", ha="center", fontsize=9, weight="bold", color=BLUE)
    save(fig, path)


def ground_model():
    fig, ax, path = canvas("data_to_ground_model", 9, 5.4)
    title(ax, "Des observations ponctuelles au modèle géotechnique argumenté")
    sources = [(3, 66, "Sondages\net carottes"), (3, 40, "CPT / PMT\net laboratoire"), (3, 14, "Géophysique\net piézométrie")]
    for x, y, text in sources: box(ax, x, y, 22, 16, text, fontsize=8.5)
    box(ax, 37, 35, 26, 30, "Modèle conceptuel\nStratigraphie\nHydrogéologie\nParamètres\nIncertitudes", fontsize=9, fill="#fff4e6", color=ORANGE)
    box(ax, 75, 35, 22, 30, "Décisions\nFondations\nProtection\nSuivi\nInvestigations complémentaires", fontsize=8.5)
    for y in [74, 48, 22]: arrow(ax, 25, y, 37, 50)
    arrow(ax, 63, 50, 75, 50)
    arrow(ax, 86, 32, 50, 27, TEAL, rad=-.18)
    ax.text(50, 4, "Toute coupe géotechnique doit distinguer ce qui est mesuré, interpolé ou supposé.", ha="center", fontsize=9, weight="bold", color=BLUE)
    save(fig, path)


def selection():
    fig, ax, path = canvas("foundation_selection", 9, 5.5)
    title(ax, "Choix comparatif des fondations")
    box(ax, 35, 72, 30, 15, "Données du projet\net niveau de confiance", fontsize=9)
    box(ax, 4, 43, 27, 18, "Superficielle\nPortance, tassements,\naffouillement, exécution", fontsize=8.3)
    box(ax, 36.5, 43, 27, 18, "Profonde\nTransfert, groupe,\ndéplacements, mise en œuvre", fontsize=8.3)
    box(ax, 69, 43, 27, 18, "Adaptation du site\nAmélioration, drainage,\nprotection ou déplacement\nd’appui", fontsize=8.3)
    arrow(ax, 50, 72, 18, 61); arrow(ax, 50, 72, 50, 61); arrow(ax, 50, 72, 82, 61)
    box(ax, 26, 13, 48, 17, "Comparer sécurité + déformations + durabilité + constructibilité + coût global + risques résiduels", fontsize=9, fill="#fff4e6", color=ORANGE)
    for x in [18, 50, 82]: arrow(ax, x, 43, 50, 30)
    ax.text(50, 4, "Une option écartée doit l’être pour une raison documentée, non par habitude.", ha="center", fontsize=9, style="italic")
    save(fig, path)


def observational():
    fig, ax, path = canvas("observational_loop", 8, 5.2)
    title(ax, "Méthode observationnelle : prévoir, mesurer, comparer, agir")
    pts = [(50, 73, "Prévisions et\nhypothèses"), (78, 50, "Instrumentation\net critères d’alerte"), (50, 20, "Mesures en\nconstruction / exploitation"), (22, 50, "Revue du modèle\net actions prévues")]
    for x, y, text in pts: box(ax, x-13, y-8, 26, 16, text, fontsize=8.5)
    arrow(ax, 62, 69, 75, 59, TEAL, rad=-.15); arrow(ax, 75, 41, 62, 28, TEAL, rad=-.15)
    arrow(ax, 38, 28, 25, 41, TEAL, rad=-.15); arrow(ax, 25, 59, 38, 69, TEAL, rad=-.15)
    ax.text(50, 48, "Boucle\ntraçable", ha="center", va="center", fontsize=11, weight="bold", color=BLUE)
    ax.text(50, 5, "Les actions à entreprendre en cas d’écart doivent être définies avant les mesures.", ha="center", fontsize=9)
    save(fig, path)


def multidisciplinary():
    fig, ax, path = canvas("multidisciplinary", 8, 6)
    title(ax, "Une reconnaissance de pont est un projet multidisciplinaire")
    box(ax, 34, 39, 32, 22, "Modèle partagé\ndu site et de l’ouvrage", fontsize=10, fill="#fff4e6", color=ORANGE)
    items = [(5, 70, "Géologue\net hydrogéologue"), (68, 70, "Hydrologue\net hydraulicien"), (3, 14, "Géotechnicien\net laboratoire"), (68, 14, "Structure, matériaux,\nexécution et inspection")]
    for x, y, text in items: box(ax, x, y, 29, 16, text, fontsize=8.5)
    for x1, y1, x2, y2 in [(28,70,43,61),(73,70,57,61),(27,30,43,39),(73,30,57,39)]: arrow(ax,x1,y1,x2,y2,TEAL,style="<|-|>")
    ax.text(50, 5, "Les hypothèses, les désaccords et les données manquantes doivent circuler entre disciplines.", ha="center", fontsize=9)
    save(fig, path)


def risk_register():
    fig, ax, path = canvas("risk_register_flow", 9, 4.8)
    title(ax, "Du danger identifié au risque résiduel documenté")
    labels = [(2,"Danger /\nmécanisme"),(22,"Données et\nincertitudes"),(42,"Conséquences\nsur l’ouvrage"),(62,"Mesures de\nmaîtrise"),(82,"Risque résiduel\net suivi")]
    for x,text in labels:box(ax,x,45,16,23,text,fontsize=8.2)
    for x in [2,22,42,62]:arrow(ax,x+16,56,x+20,56)
    ax.text(50,28,"Une matrice peut prioriser une revue ; elle ne déduit pas automatiquement une catégorie géotechnique réglementaire.",ha="center",fontsize=9,weight="bold",color=BLUE)
    ax.text(50,13,"Chaque ligne doit avoir un responsable, une preuve, une échéance et un critère de clôture.",ha="center",fontsize=9)
    save(fig,path)


def fluvial_system():
    fig, ax, path = canvas("fluvial_system", 10, 5.1)
    title(ax, "Du bassin versant à la fondation : chaîne hydrologique et morphodynamique")
    labels = [
        (2, "Bassin versant\nPluie, relief, sols, occupation"),
        (22, "Hydrologie\nDébits et scénarios de crue"),
        (42, "Hydraulique\nNiveaux, vitesses, contraintes"),
        (62, "Morphodynamique\nTransport solide et mobilité du lit"),
        (82, "Appui et fondation\nGéométrie future et protection"),
    ]
    for x, text in labels:
        box(ax, x, 48, 16, 24, text, fontsize=8.1)
    for x in [2, 22, 42, 62]:
        arrow(ax, x+16, 60, x+20, 60)
    ax.text(50, 31, "Les scénarios et leurs incertitudes doivent circuler dans toute la chaîne.", ha="center", fontsize=9, weight="bold", color=BLUE)
    ax.text(50, 16, "Une période de retour ne résume ni la durée de la crue, ni le volume de transport solide, ni la forme future du chenal.", ha="center", fontsize=9)
    save(fig, path)


def karst_model():
    fig, ax, path = canvas("karst_ground_model", 9, 5.6)
    title(ax, "Karst : distinguer processus géologique, preuves et conséquences pour l’appui")
    ax.add_patch(Rectangle((0, 55), 100, 14, facecolor=SAND, edgecolor="none"))
    ax.add_patch(Rectangle((0, 10), 100, 45, facecolor="#c8c5b8", edgecolor="none"))
    ax.text(8, 62, "Couverture : remaniement et affaissement possibles", fontsize=8.5)
    ax.text(8, 49, "Calcaire : dissolution le long des discontinuités", fontsize=8.5)
    for x in [25, 48, 73]:
        ax.plot([x, x+5], [55, 20], color=DARK, lw=.8, alpha=.65)
    ax.add_patch(Polygon([[42, 36], [48, 44], [60, 42], [66, 30], [59, 19], [47, 22]], facecolor="white", edgecolor=RED, lw=1.4))
    ax.text(54, 32, "Cavité ou zone altérée\nà caractériser", ha="center", fontsize=8.5, color=RED)
    ax.plot([54, 54], [69, 15], color=BLUE, lw=1.5, ls="--")
    ax.add_patch(Rectangle((49, 69), 10, 5, facecolor=ORANGE, edgecolor=DARK))
    ax.text(60, 76, "Sondage de vérification", fontsize=8.5, color=BLUE)
    ax.plot([0, 100], [52, 52], color=TEAL, lw=1, ls="--")
    ax.text(77, 58, "Eau : dissolution, remplissage\net variations de nappe", fontsize=8.5, color=BLUE)
    ax.text(50, 5, "Le risque dépend de la géométrie, du remplissage, de l’eau, des charges et de l’évolution — pas d’un seul rapport géométrique.", ha="center", fontsize=8.8, weight="bold")
    save(fig, path)


def evidence_decisions():
    fig, ax, path = canvas("evidence_based_decisions", 10, 5.2)
    title(ax, "De la source à une décision proportionnée à la preuve")
    steps = [
        (3, "1. Identifier", "Auteur, titre, édition, date\net identifiant de la source"),
        (28, "2. Contrôler", "Intégrité, procédure, cohérence\net concordance avec d’autres sources"),
        (53, "3. Délimiter", "Site, méthode, population,\nhypothèses et limites"),
        (78, "4. Décider", "Retenir, corriger, restreindre,\ncompléter ou écarter"),
    ]
    for x, heading, text in steps:
        box(ax, x, 50, 19, 27, heading + "\n" + text, fontsize=8.4)
        if x < 78:
            arrow(ax, x + 19.5, 63.5, x + 24, 63.5)
    examples = [
        (6, "Texte officiel", "Exigence dans son champ et à sa date d’application"),
        (38, "Article scientifique", "Résultat lié aux matériaux, essais et modèle étudiés"),
        (70, "Article de presse", "Événement rapporté, sans expertise causale implicite"),
    ]
    for x, heading, text in examples:
        box(ax, x, 15, 24, 20, heading + "\n" + text, color=TEAL, fontsize=8.2, fill="#f4f8f9")
    ax.text(50, 5, "Une information exacte peut être inutilisable si elle est sortie de son domaine.", ha="center", fontsize=9, weight="bold", color=DARK)
    save(fig, path)


def main():
    for function in [history, four_families, components, foundation_alternatives, load_path,
                     valley, fluvial_system, karst_model, workflow, tests, geophysics, risks, scour, erosion,
                     liquefaction, ground_model, selection, observational,
                     multidisciplinary, risk_register, evidence_decisions]:
        function()
        print(f"GENERATED {function.__name__}")
    print(f"FIGURES {len(list(OUT.glob('*.png')))} in {OUT}")

if __name__ == "__main__":
    main()
