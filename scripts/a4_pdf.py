"""HTML (pages SVG A4) -> PDF avec Chrome/Edge headless, puis une PNG par page pour le controle visuel.

    python a4_pdf.py fiches/Fiche-TP1.html [dossier_png]

Les PNG (Fiche-TP1_1.png, _2.png...) sont a REGARDER apres chaque rendu :
textes qui se chevauchent, debordements, courbes coupees.
Besoin : pymupdf (pip install pymupdf) pour les PNG.
"""
import os
import pathlib
import shutil
import subprocess
import sys

CANDIDATS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def navigateur():
    for c in CANDIDATS:
        if os.path.exists(c):
            return c
    for nom in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        p = shutil.which(nom)
        if p:
            return p
    sys.exit("Chrome, Chromium ou Edge introuvable.")


def main():
    html = pathlib.Path(sys.argv[1]).resolve()
    pdf = html.with_suffix(".pdf")
    png_dir = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else html.parent / "_controle"
    subprocess.run([navigateur(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", html.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("PDF :", pdf)
    try:
        import fitz
    except ImportError:
        print("pymupdf absent : pas de PNG de controle (pip install pymupdf)")
        return
    png_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        out = png_dir / f"{html.stem}_{i}.png"
        page.get_pixmap(dpi=110).save(out)
        print("PNG :", out)
    print(len(doc), "page(s)")


if __name__ == "__main__":
    main()
