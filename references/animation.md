# Livrable 4 : animations vidéo (seulement sur demande)

**But :** une vidéo par TP, avec voix, qui déroule le TP **dans l'ordre du fascicule**, comme la vidéo du prof. Commence par **une démo sur le premier TP**, attends qu'il la valide, puis fais les autres.

## Outils (`scripts/`)

| Fichier | Rôle |
|---|---|
| `scene_base.py` | classe `SceneTP` : voix synchronisée (`speak`, `sync`), parties (`partie`), étapes (`etape`), récapitulatif (`panel_add`), curseurs d'oscillo (`curseur_t`), axes `Stage` |
| `voix.py` | `extraits` pour choisir la voix, `generer` pour les mp3 et leurs durées, `mixer` pour la vidéo finale |

Installation (deux environnements séparés, dans le dossier `animations/`) :

```bash
python -m venv .manim-venv && .manim-venv/Scripts/pip install manimgl
python -m venv .voice-venv && .voice-venv/Scripts/pip install edge-tts
# il faut aussi ffmpeg dans le PATH (et, pour manimgl, Pango et un pilote OpenGL)
```

## Déroulé

1. **Choisir la voix** : `python voix.py extraits` produit 5 extraits. Il écoute et choisit. Remy est la voix la plus naturelle par défaut. Edge-tts est gratuit et passe par Internet.
2. **Relever les couleurs du prof** : extrais des images de sa vidéo avec ffmpeg, lis la couleur des pixels de chaque élément (entrée, mesure, écart, fonction de transfert, paramètres), et note-les en tête de la scène. Le fond est noir. **Exception** : les bornes et les câbles gardent les couleurs du vrai matériel.
3. **Écrire la narration** dans `<nom>_narration.py`, sous la forme `NARRATION = {"cle": "phrase", …}` :
   - une phrase par idée, à voix haute, dans l'ordre du fascicule ;
   - les nombres écrits **comme on les lit**, avec une virgule (« 1,3 hertz », « moins 6 volts »), jamais « 1.3 » ;
   - les sigles épelés si besoin (« T P 1 »).
4. **Écrire la scène** (`<nom>.py`, une classe qui hérite de `SceneTP`), en séparant **vraiment** les parties :
   - `partie(i, cle)` : écran noir, puis le plan avec la partie en cours ;
   - `etape("ON RAJOUTE", "fil 3")`, `etape("ON MODIFIE", "K = 40")`, `etape("ON MESURE", "τ")`, `etape("ON ALLUME", fort=True)` : chaque étape efface la précédente et s'annonce ;
   - `garder=[…]` pour ce qui doit rester d'une étape à l'autre (le câblage déjà posé, par exemple) ;
   - `panel_add(…)` pour les résultats qui s'accumulent à droite ;
   - les vraies courbes (CSV), les curseurs de l'oscillo, puis les valeurs du CR **vérifiées**.
5. **Fabriquer la vidéo** :
   ```bash
   .voice-venv/Scripts/python voix.py generer TP1 Remy
   $env:VOIX="Remy"; .manim-venv/Scripts/manimgl TP1.py TP1 -w --hd --video_dir voix/TP1/Remy --file_name muet
   .voice-venv/Scripts/python voix.py mixer TP1 Remy        # -> TP1-Remy.mp4
   ```
6. **Contrôler** :
   - extraire des images à quelques instants (`ffmpeg -ss 30 -i … -frames:v 1`) et vérifier fond, textes coupés, éléments qui disparaissent trop tôt ;
   - transcrire le son avec faster-whisper pour vérifier la prononciation. Attention, certaines erreurs sont des homophones de whisper et pas des fautes de la voix (« abaque » entendu « la bague »).
7. Livrer : durée, plan, et « Tu valides ? ». Quand une seule phrase change, `generer` ne refait que celle-là.

## Pièges rencontrés

- Fond gris par défaut : il faut `default_camera_config = dict(background_color=BLACK)`, déjà mis dans `SceneTP`.
- Un récapitulatif qui s'efface à chaque étape : il faut l'ajouter avec `panel_add`, pas avec `add`.
- Sous Windows, la commande ffmpeg devient trop longue s'il y a beaucoup de phrases. Le filtre audio passe donc par un fichier (`voix.py` le fait déjà).
