# Livrable 5 : partiel d'entraînement et corrigé

**But :** un partiel blanc **dans le vrai format**, qu'il peut faire **chez lui sans paillasse**. C'est toi qui dessines les oscillogrammes, c'est lui qui lit les valeurs.

## A. Le sujet (`fiches/Partiel-entrainement.pdf`)

Reprends exactement ce qu'il a confirmé au démarrage : durée, QCM, nombre de bonnes réponses, points négatifs, documents autorisés.

**Page de garde** : durée, barème, consignes (« Toute valeur calculée : formule, application numérique, unité »).

**Partie 1, le QCM sur feuille**. Elle se fait sans paillasse, donc les figures sont imprimées sur la feuille.
- Environ 20 questions qui couvrent **tous les TP** du partiel. Mélange :
  - des questions de lecture de courbe (identifier l'ordre, l'effet de z ou de ωn) ;
  - des calculs courts (s(∞), TR5% = 3τ, K…) ;
  - des questions de méthode (curseur à 0,63 · m(∞)) ;
  - des questions de compréhension (pourquoi U ≠ 0 alors que E = 0 ; classe ; saturation).
- Une seule bonne réponse si c'est le format. Les distracteurs sont **les erreurs classiques** : niveau au lieu de variation, ms au lieu de s, racine oubliée.
- Barème affiché, par exemple +0,4 / −0,2 / 0.

**Partie 2, la pratique**. Un exercice par TP, dans l'ordre des TP.
- **Un seul modèle cohérent** sert à tous les exercices : le même moteur, avec G0, z et ωn fixés. Ses valeurs se retrouvent d'un exercice à l'autre (BO, puis BF avec P, puis PI…). Simule-le en Python (2nd ordre, boucle fermée, saturation, PI, perturbation) et garde le script.
- **Oscillogrammes dessinés** avec `osc()` : écran de 10 × 8 div, calibres affichés, couleurs des voies, léger bruit. Les valeurs ne sont **pas** écrites, il doit les lire. Choisis des calibres qui donnent des lectures faisables, à ±0,2 div près.
- Questions numérotées comme au TP, avec les points de chaque question. Des questions de lecture, de calcul, de comparaison avec la théorie et de conclusion (« cahier des charges respecté ? »).
- Mets au moins **un piège réaliste** par exercice : un passage à 95 % qui n'est pas le TR5%, deux calibres différents, Tp/2 au lieu de Tp.
- **Annexe** : les abaques du fascicule, en image.

## B. La correction cachée (`.correction/Partiel-entrainement-correction.md`)

- Mets le dossier `.correction/` en caché (sous Windows : `attrib +h .correction`). Préviens-le une fois : « n'ouvre pas `.correction/` ».
- Pour chaque question, écris :
  - la **valeur exacte** tirée de la simulation et la **tolérance** de lecture ;
  - le calcul ;
  - deux indices gradués ;
  - le piège ;
  - la source dans ses documents.
- Génère ce fichier **depuis le script de simulation**, pour que les valeurs soient exactement celles des figures.
- **Ne montre jamais son contenu** tant qu'il ne demande pas le corrigé.

## C. Corriger sa copie

Il compose de son côté, puis envoie ses réponses, en texte ou en photo.

**QCM** : il donne souvent ses réponses **par morceaux**. Corrige seulement ce qu'il a envoyé et **ne dis rien des questions suivantes**. Pour chaque réponse fausse ou vide :
- explique pourquoi, en 2 ou 3 lignes ;
- s'il ne comprend toujours pas, réexplique **autrement**, avec un dessin en texte ou un exemple chiffré, au lieu de répéter.

À la fin, donne la note avec le barème, et calcule-la : `12 justes × 0,4 − 3 fausses × 0,2`.

**Pratique** : corrige question par question, au format :
```
formule de base => formule isolée
                => application numérique
```
🟥 **résultat avec unité**

Une lecture juste à la tolérance près compte comme juste. Une unité fausse compte comme fausse. Donne la note sur 20 et les 2 ou 3 notions à revoir, puis mets à jour `progression.md`.

## D. Fiche « Questions QCM pas réussies »

Après la correction du QCM, propose **une page A4** avec une case par question ratée ou laissée vide. Chaque case contient :
- un mini-dessin ;
- la formule ;
- la méthode en 3 étapes ;
- le résultat encadré ;
- le piège, en rouge.

Tu peux aussi ajouter une case pour une question qu'il a posée pendant la correction (« différence entre gain statique et erreur statique »).

## E. Le corrigé A4 (`fiches/Partiel-entrainement-CORRIGE.pdf`), seulement s'il le demande

- **Page 1, le QCM** : la lettre dans une pastille rouge, la bonne réponse, la raison en une ligne et **sa réponse** (✓ en vert, ✗ en rouge, vide en gris), puis le calcul de sa note.
- **Pages suivantes, la pratique** : **les mêmes figures que le sujet**, annotées en rouge. On y voit :
  - les niveaux (0,63, 0,95, tube ±5 %), avec les lignes pointillées et la croix ou le point lu ;
  - les doubles flèches de lecture (τ, TR5%, Tp/2, D1, angle mort) ;
  - le piège montré sur la figure (« 168 ms : PAS le TR5% »).

  À côté de chaque question, une `carte` avec le calcul et le **résultat encadré**. Les abaques sont tracés avec les flèches de lecture.
- S'il demande « le corrigé » **avant** d'avoir fait la pratique, donne-le, puis conseille-lui en une ligne de refaire les exercices sans le regarder.

## F. Après le partiel blanc

Si le partiel approche, propose un **plan** en une ligne : refaire tel exercice chronométré, puis relire la fiche À retenir, puis dormir.
