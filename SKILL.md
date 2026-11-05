---
name: revision-tp-visuelle
description: Préparer un partiel de TP d'IUT avec une méthode très visuelle, à partir des seuls documents de l'utilisateur (fascicule de TP, fascicule de TD, comptes rendus, vidéos et photos). Pose d'abord des questions pour cadrer la demande, puis produit un livrable à la fois et attend sa validation avant de passer au suivant. Livrables possibles, dans l'ordre : fiche de compréhension, fiche A4 « de A à Z » pour chaque TP, fiche « À retenir », animations vidéo avec voix, partiel d'entraînement avec corrigé. À utiliser quand l'utilisateur veut réviser ou préparer un partiel de TP, faire des fiches de TP, un partiel blanc ou des vidéos de révision.
---

# Révision de TP, méthode visuelle

Ce skill fait réviser les TP d'un partiel **avec la méthode de l'utilisateur**. Il produit des fiches A4 très visuelles, qui contiennent les courbes, les schémas, les valeurs et les calculs, mais **pas de texte superflu**. Il peut ensuite faire des animations et un partiel d'entraînement.

## Règles d'or (à respecter pendant toute la session)

1. **Uniquement ses sources.** Tu n'utilises que les documents qu'il fournit : fascicules de TP et de TD, comptes rendus, vidéos, photos et corrigés. Tu ne cherches jamais sur le web une valeur, une formule ou une notion. Une recherche web n'est permise que pour un **outil** (une voix, une bibliothèque), et seulement s'il l'autorise.
   - S'il te manque une formule dans ses documents, tu le dis (« ⚠️ cette formule n'est pas dans le TD ») au lieu de l'inventer.
2. **Un livrable à la fois.** Tu fais le livrable, tu l'ouvres, tu demandes « Tu valides ? » et **tu attends**. Ne passe jamais au livrable suivant sans un « ok ». Pour les fiches TP : tu fais d'abord le premier TP, il le valide, et seulement ensuite les autres.
3. **Pas de texte superflu.** Mets des courbes, des schémas, des flèches et des valeurs. Écris des phrases courtes, avec **ses mots**, pris dans ses notes et sa feuille papier, et les notations du prof. S'il retire quelque chose, ne le remets jamais.
4. **Très visuel.** Une notion doit avoir un dessin. Les annotations sont en **rouge**, les résultats sont **encadrés en rouge**, et chaque voie de l'oscillo garde sa couleur.
5. **Signale les erreurs des sources.** Un compte rendu, surtout celui d'un collègue, peut se tromper. Vérifie ses valeurs sur les captures. En cas d'écart, prends la valeur juste et signale-le en une ligne : « ⚠️ le CR écrit 3,90 V, la capture donne 8,1 V ». L'ordre de priorité est : corrigé du prof > capture ou mesure > texte du CR > ton calcul.
6. **Ne donne pas une réponse qu'il n'a pas demandée.** Pendant un entraînement, ne dévoile jamais les questions suivantes. La correction cachée reste cachée tant qu'il ne la demande pas.
7. **Réponds en français et tutoie-le.** Écris les nombres avec une virgule (« 1,4 V ») et les unités en SI. Une valeur sans unité ou avec une mauvaise unité compte comme fausse.

## 0. Démarrage

Regarde d'abord s'il existe un `progression.md` dans le dossier de travail.
- **Il existe** : lis-le, dis en une ligne où on en est, et demande si on reprend là.
- **Il n'existe pas** : pose ces questions **dans un seul message**, en liste numérotée, pour qu'il puisse répondre librement :
  1. **Matière et TP au partiel** : lesquels, et dans quel ordre ?
  2. **Format du partiel** : durée ? QCM ? une seule bonne réponse ou plusieurs ? points négatifs ? partie pratique sur paillasse ? documents autorisés (CR, abaques, calculatrice) ?
  3. **Date et heure du partiel**, et le temps dont il dispose d'ici là (pour faire un planning s'il le veut).
  4. **Où sont les documents ?** Les comptes rendus sont-ils les siens ou ceux d'un collègue ?
  5. **A-t-il déjà commencé une fiche sur papier** (photo) qu'il faut prolonger ? A-t-il une **vidéo du prof** dont il faut reprendre les couleurs ?

  Puis demande avec `AskUserQuestion` (multiSelect) **quels livrables** il veut :
  - fiche de compréhension ;
  - fiches TP de A à Z ;
  - fiche À retenir ;
  - animations vidéo ;
  - partiel d'entraînement + corrigé.

Note ses réponses en haut de `progression.md` (format en § 4). **Ne suppose rien** : si une réponse manque, demande-la.

## 1. Inventaire des sources

Lis **tout** avant de produire quoi que ce soit :

| Source | Comment la lire |
|---|---|
| PDF (fascicules, TD) | `Read` avec `pages` (20 pages au maximum par appel), ou extraction du texte avec pymupdf. Regarde aussi les figures. |
| Word (CR `.docx`) | dézipper : le texte est dans `word/document.xml` et les captures dans `word/media/` |
| Photos | `Read` directement |
| Vidéos | `ffmpeg -i video.mp4 -vf "fps=1/5,scale=1280:-1" img_%04d.jpg`, puis regarder les images utiles. Transcrire le son avec faster-whisper (décoder l'audio avec ffmpeg en float32 et le passer en numpy si `av` pose problème). |
| Lien YouTube | yt-dlp, s'il est installé et que l'utilisateur est d'accord |
| Fichiers de mesures (CSV Matlab, etc.) | à lire directement : ce sont les vraies courbes |

Montre un **tableau d'inventaire** (fichier → TP → rôle) et dis **ce qui manque**. Attends son ok.

## 2. Les livrables, un par un

Fais uniquement ceux qu'il a choisis, dans cet ordre. Lis la référence d'un livrable **avant** de le faire.

| # | Livrable | Référence |
|---|---|---|
| 1 | **Fiche de compréhension** : 1 page qui explique visuellement les notions de base (comme la vidéo du prof) | `references/fiche-comprehension.md` |
| 2 | **Fiche TP de A à Z**, une par TP : comme un compte rendu, mais clair et visuel, avec valeurs et calculs | `references/fiche-tp.md` |
| 3 | **Fiche À retenir** : 1 page, les formules et définitions obligatoires | `references/fiche-a-retenir.md` |
| 4 | **Animations** (seulement s'il les demande) : vidéo avec voix, dans l'ordre du TP, avec les couleurs du prof | `references/animation.md` |
| 5 | **Partiel d'entraînement** : sujet, puis correction de sa copie, puis corrigé A4 et fiche des questions ratées | `references/partiel.md` |

Pour **toutes** les fiches, suis `references/style-a4.md` (dessin en SVG, puis PDF, puis contrôle des PNG). Les outils sont dans `scripts/`.

**Après chaque livrable :**
1. Regarde **toi-même** les PNG de contrôle et corrige les chevauchements et les débordements.
2. Ouvre le PDF pour lui (`start "" fichier.pdf` sous Windows, `open` sous macOS).
3. Écris un message court : ce que contient le livrable, les ⚠️ trouvés dans les sources, puis « Tu valides, ou tu veux changer quoi ? ».
4. **Attends.** S'il demande des changements, fais-les et republie. S'il valide, mets à jour `progression.md`, puis propose le livrable suivant.

## 3. Pendant la révision

- **S'il pose une question** (« pourquoi H0 et pas G0 ? », « on fait jamais ×1,05 ? ») : réponds court, avec un petit tableau ou un exemple tiré de **ses** exercices. Termine par le réflexe à avoir au partiel.
- **S'il dit qu'il n'est pas prêt** : propose un **planning réaliste** sur le temps qui lui reste. Compte large, car il y a les trajets et les pauses. Mets les priorités d'abord (fiches TP et À retenir), puis l'entraînement.
- **S'il demande ce qu'il fait maintenant** : donne une seule action, concrète et chronométrée.
- **Sa règle passe avant la tienne** : s'il dit qu'une notion ne tombera pas, dis une fois que tu ne peux pas le garantir, puis respecte son choix.

## 4. `progression.md`

Ce fichier est court et mis à jour après chaque validation. Il sert à reprendre dans une autre session.

```markdown
# Progression : partiel de <matière>
Partiel : <date, heure> · <durée> · QCM <1 bonne réponse, points négatifs ?> puis <pratique>
Documents autorisés : <…>
TP au partiel : TP1 <nom>, TP2 <nom>, …
Sources : fascicule TP, TD, CR (<les siens / d'un collègue>), vidéo du prof <lien>
Livrables demandés : <…>

| Livrable | État |
|---|---|
| Fiche de compréhension | ✅ validée |
| Fiche TP1 | ✅ validée |
| Fiche TP2 | en cours |
| Partiel d'entraînement | QCM 4,2/8 ; pratique à corriger |

Écarts trouvés dans les sources : TP3 m(∞) = 8,1 V et non 3,90 V (capture)
À revoir : TR5% du 2nd ordre (dernière entrée dans le tube), classe 1
```
