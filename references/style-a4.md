# Style des fiches A4

## Chaîne de fabrication

1. **Un script Python par fiche**, que tu gardes, par exemple `fiche_tp1.py` dans le scratchpad ou dans un dossier `outils/`. Il importe `scripts/a4.py` et dessine chaque page en SVG de 1000 × 1414.
2. `ecrire(titre, "fiches/Fiche-TP1.html")`, puis `python scripts/a4_pdf.py fiches/Fiche-TP1.html <dossier_png>`. Tu obtiens le PDF et **une PNG par page**.
3. **Regarde chaque PNG** avec `Read`. Corrige les textes qui se chevauchent, ceux qui sortent du cadre, les courbes coupées et les étiquettes posées sur une courbe. Recommence le rendu jusqu'à ce que tout soit propre. Ne livre jamais une fiche sans avoir regardé ses PNG.
4. Les livrables vont dans `fiches/` : `Fiche-comprehension.pdf`, `Fiche-TP1-A-a-Z.pdf`, `Fiche-A-retenir.pdf`, `Partiel-entrainement.pdf`, `Partiel-entrainement-CORRIGE.pdf`. Le HTML peut rester à côté.

Dépendances : Python 3, `pymupdf` et `pillow`, plus Chrome ou Edge pour l'export PDF.

## Ce qu'on voit sur la page

| Élément | Règle |
|---|---|
| Titre | en haut à gauche, en gras ; à droite, en rouge, le TP ou la partie |
| Courbes | toujours avec des **valeurs** : axes gradués, niveaux (0,63 · m(∞), 0,95 · m(∞)…) et temps lus |
| Voies de l'oscillo | voie 1 jaune, voie 2 verte, voie 3 bleue, voie 4 rose, comme sur l'appareil (`V1` à `V4`) |
| Annotations | en **rouge** : curseurs pointillés, doubles flèches pour un écart, point sur la valeur lue |
| Résultat | **encadré en rouge** (`carte(..., res=...)`) |
| Calcul | formule de base ⇒ formule retournée ⇒ application numérique ⇒ résultat avec unité |
| Notes | en gris, une ligne. Un piège s'écrit en rouge : « Piège : … » |
| Formules | en police mathématique (`M`), avec `_{0}` pour les indices et `^{2}` pour les exposants |
| Schémas | les blocs du fascicule (comparateur, régulateur, ampli, moteur, capteur). Les câbles sont numérotés avec des pastilles rouges (`badge`) aux vraies couleurs des bornes. |
| Captures du CR | à insérer si elles sont lisibles (aplatir la transparence sur fond blanc), avec un recadrage. Sinon, les redessiner. |
| Figures colorées du fascicule (Simulink…) | à reprendre **avec leurs couleurs** et une légende des couleurs. Vérifier sur l'image, pas dans le texte du CR. |

## Ce qu'on ne met pas

- de paragraphe d'explication : une flèche et 3 mots suffisent ;
- de rappel de matériel ni de réglage, sauf s'il le demande ;
- une notion qui n'est pas dans ses documents ;
- une formule qui n'est pas dans le TD sans le ⚠️ qui le signale.

## Reprendre les vraies courbes

- **Un fichier de mesures** (CSV Matlab, etc.) est la meilleure source : trace-le directement, avec un petit lissage.
- **Une capture d'oscilloscope** : cale l'échelle en pixels par division sur la grille (compte les pixels entre deux traits). Repère t = 0, au front de l'échelon ou au curseur X1, puis extrais la courbe en filtrant la couleur de la voie. Vérifie la courbe extraite en la superposant à la capture.
- **Si la capture contredit le texte du CR**, la capture a raison : signale-le.

## Pour les allures théoriques

`s2(t, H0, z, wn)` donne une réponse du 2nd ordre, et `1 - exp(-t/τ)` une réponse du 1er ordre. Ces fonctions servent à dessiner l'effet d'un paramètre (z, ωn, K), jamais à fabriquer une « mesure ».
