"""Voix des animations avec edge-tts (voix neuronales Microsoft, gratuites, en ligne).
Ne regenere que les phrases modifiees.

Dans le dossier des animations (ou le texte est dans <nom>_narration.py, dict NARRATION) :

  python voix.py generer TP1 Remy          -> voix/TP1/Remy/*.mp3 + durees.json
  (rendu manim : la scene lit durees.json et ecrit timeline.json, video muette voix/TP1/Remy/muet.mp4)
  python voix.py mixer TP1 Remy            -> TP1-Remy.mp4
  python voix.py extraits                  -> extraits-voix/*.mp3 pour choisir la voix

Voix : Denise, Eloise, Henri, Remy, Vivienne. Ecrire les nombres comme on les lit (« 1,3 » et non « 1.3 »).
Besoin : pip install edge-tts ; ffmpeg et ffprobe dans le PATH.
"""
import asyncio
import importlib
import json
import pathlib
import subprocess
import sys

import edge_tts

ICI = pathlib.Path.cwd()
IDS = {
    "Denise": "fr-FR-DeniseNeural",
    "Eloise": "fr-FR-EloiseNeural",
    "Henri": "fr-FR-HenriNeural",
    "Remy": "fr-FR-RemyMultilingualNeural",
    "Vivienne": "fr-FR-VivienneMultilingualNeural",
}
EXTRAIT = "Le gain statique G zéro vaut 0,15 : la mesure finale divisée par l'échelon d'entrée."


def duree(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


async def generer(nom, voix, dossier):
    sys.path.insert(0, str(ICI))
    textes = importlib.import_module(f"{nom}_narration").NARRATION
    dossier.mkdir(parents=True, exist_ok=True)
    f_textes = dossier / "textes.json"
    anciens = json.loads(f_textes.read_text(encoding="utf-8")) if f_textes.exists() else {}
    durees, n = {}, 0
    for cle, texte in textes.items():
        path = dossier / f"{cle}.mp3"
        if anciens.get(cle) != texte or not path.exists():
            await edge_tts.Communicate(texte, IDS[voix]).save(str(path))
            n += 1
        durees[cle] = duree(path)
    f_textes.write_text(json.dumps(textes, ensure_ascii=False, indent=0), encoding="utf-8")
    (dossier / "durees.json").write_text(json.dumps(durees, indent=0), encoding="utf-8")
    print(f"{len(durees)} phrases ({n} regenerees), {sum(durees.values()):.1f} s de voix")


def mixer(nom, voix, dossier):
    timeline = json.loads((dossier / "timeline.json").read_text(encoding="utf-8"))
    video = dossier / "muet.mp4"
    sortie = ICI / f"{nom}-{voix}.mp4"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video)]
    filtres = []
    for i, (debut, cle) in enumerate(timeline):
        cmd += ["-i", str(dossier / f"{cle}.mp3")]
        filtres.append(f"[{i + 1}:a]adelay={round(debut * 1000)}:all=1[a{i}]")
    entrees = "".join(f"[a{i}]" for i in range(len(timeline)))
    filtres.append(f"{entrees}amix=inputs={len(timeline)}:normalize=0[voix]")
    # filtre dans un fichier : la ligne de commande devient trop longue sous Windows
    script = dossier / "filtre.txt"
    script.write_text(";".join(filtres), encoding="utf-8")
    cmd += ["-/filter_complex", str(script), "-map", "0:v", "-map", "[voix]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(sortie)]
    subprocess.run(cmd, check=True)
    print(sortie.name, f"{duree(sortie):.1f} s (video muette : {duree(video):.1f} s)")


async def extraits():
    d = ICI / "extraits-voix"
    d.mkdir(exist_ok=True)
    for nom, vid in IDS.items():
        await edge_tts.Communicate(EXTRAIT, vid).save(str(d / f"{nom}.mp3"))
        print(d / f"{nom}.mp3")


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "extraits":
        asyncio.run(extraits())
    else:
        nom, voix = sys.argv[2:4]
        dossier = ICI / "voix" / nom / voix
        if action == "generer":
            asyncio.run(generer(nom, voix, dossier))
        else:
            mixer(nom, voix, dossier)
