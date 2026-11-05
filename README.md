# revision-tp-visuelle

Un skill [Claude Code](https://code.claude.com/docs/en/skills) pour préparer un **partiel de TP** (IUT, BUT, BTS…) avec une méthode **très visuelle** : des courbes, des schémas, des valeurs et des calculs encadrés, sans texte superflu.

Il travaille **uniquement avec tes documents** : fascicule de TP, fascicule de TD, comptes rendus, vidéos et photos. Il ne va jamais chercher une formule sur Internet.

## Ce qu'il fait

1. **Il te pose des questions** : quels TP sont au partiel, la durée, le format du QCM (points négatifs ? une seule bonne réponse ?), les documents autorisés, la date, et ce que tu veux qu'il produise.
2. **Il lit tous tes documents** et te montre l'inventaire, avec ce qui manque.
3. **Il produit un livrable à la fois**, puis il attend que tu le valides avant de passer au suivant :

| # | Livrable | Format |
|---|---|---|
| 1 | **Fiche de compréhension** : les notions de base en dessins, comme la vidéo du prof | 1 page A4 |
| 2 | **Fiche TP de A à Z**, une par TP : comme un compte rendu, mais clair, avec les vraies courbes, les curseurs, les valeurs, les calculs et les résultats encadrés | 2 à 4 pages A4 par TP |
| 3 | **Fiche À retenir** : toutes les formules et définitions obligatoires | 1 page A4 |
| 4 | **Animations** (sur demande) : vidéo avec voix, dans l'ordre du TP, avec les couleurs du prof, des parties bien séparées (`ON RAJOUTE`, `ON MODIFIE`) | MP4 |
| 5 | **Partiel d'entraînement** : QCM sur feuille et partie pratique avec oscillogrammes dessinés (c'est toi qui lis les valeurs), puis correction de ta copie, fiche des questions ratées et corrigé A4 annoté | PDF |

Il signale les erreurs qu'il trouve dans les comptes rendus, par exemple : « ⚠️ le CR écrit 3,90 V, la capture donne 8,1 V ». Il note ta progression dans `progression.md`, ce qui te permet de reprendre dans une autre session.

## Installation

```bash
git clone https://github.com/AMATEPaul/revision-tp-visuelle.git ~/.claude/skills/revision-tp-visuelle
```

Ensuite, dans Claude Code, tape `/reload-skills` ou redémarre la session.

## Utilisation

Mets tes documents dans un dossier, ouvre Claude Code dedans, puis tape :

```
/revision-tp-visuelle
```

## Prérequis

| Pour… | Il faut |
|---|---|
| les fiches PDF | Python 3, `pip install pymupdf pillow`, Chrome ou Edge |
| lire les vidéos | [`ffmpeg`](https://ffmpeg.org/) ; pour transcrire le son, `pip install faster-whisper` (optionnel) |
| les animations | `pip install manimgl` (ManimGL) et `pip install edge-tts` (voix gratuites, connexion Internet nécessaire) |

## Contenu

| Fichier | Rôle |
|---|---|
| `SKILL.md` | la méthode : questions de départ, règles, ordre des livrables, validations |
| `references/*.md` | le détail de chaque livrable et le style des fiches |
| `scripts/a4.py` | dessin des pages A4 en SVG : oscillogrammes, courbes Matlab, curseurs, cartes de calcul avec résultat encadré |
| `scripts/a4_pdf.py` | export HTML → PDF et PNG de contrôle |
| `scripts/scene_base.py` | base des animations ManimGL : voix synchronisée, parties, étapes, curseurs |
| `scripts/voix.py` | génération des voix (edge-tts) et assemblage de la vidéo |

> Aucun document de cours n'est inclus. Le skill travaille seulement avec les tiens.

## Licence

MIT
