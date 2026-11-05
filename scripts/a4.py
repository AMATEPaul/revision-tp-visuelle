"""Bibliotheque de dessin pour les fiches A4 (SVG 1000 x 1414 par page, puis PDF via a4_pdf.py).

Utilisation dans un script de fiche :

    import sys; sys.path.insert(0, r"<dossier du skill>/scripts")
    from a4 import *

    open_page()
    entete("Fiche TP1", "Moteur à courant continu")
    p = Plot(80, 140, 400, 260, tmax=0.08, ymax=1.2)
    p.curve(lambda t: 1 - math.exp(-t / 0.012), V2)
    carte(540, 140, 430, "1.2", "τ", "0,5 pt",
          ["ΔY = 0,63 × m(∞) = 0,63 × 1,8", "     = 1,13 V"], "τ ≈ 12 ms")
    fin_page()
    ecrire("Fiche TP1", "fiches/Fiche-TP1.html")

Puis : python a4_pdf.py fiches/Fiche-TP1.html   (PDF + PNG de controle a regarder)

Conventions : _{x} = indice, ^{x} = exposant. Nombres avec une virgule.
"""
import math
import re

W, H = 1000, 1414
INK, GREY, LIGHT, RED = "#1b1b1b", "#6e6e6e", "#b9b9b9", "#c8102e"
GRN, BLUE, PINK = "#2f9e44", "#2563c9", "#c2267e"
# voies de l'oscilloscope (couleurs des voies Keysight)
V1, V2, V3, V4 = "#b88f00", "#1f9d3a", "#2563c9", "#c2267e"
YEL = "#e8b800"
MATH = "Cambria Math, Cambria, 'Times New Roman', serif"
SANS = "'Segoe UI', Arial, sans-serif"

svg = []
pages = []

DEFS = (
    "<defs>"
    + "".join(
        f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{s}" markerHeight="{s}" '
        f'orient="auto-start-reverse"><path d="M0 0.8 L9.6 5 L0 9.2 z" fill="{c}"/></marker>'
        for i, c, s in (("ah", INK, 7), ("ar", RED, 7), ("ars", RED, 5), ("ag", GRN, 6))
    )
    + "</defs><style>text{paint-order:stroke;stroke:#fff;stroke-width:2px;stroke-linejoin:round}</style>"
)


# ---------------------------------------------------------------- texte
def nu(s):
    """Texte sans les balises _{ } ^{ } (pour estimer une largeur)."""
    return re.sub(r"[_^]\{|\}", "", s)


def rich(s, size):
    parts = re.split(r"([_^]\{[^}]*\})", s)
    out, shift = [], 0
    for p in parts:
        if not p:
            continue
        if p[0] in "_^" and p[1:2] == "{":
            d = round(size * (0.28 if p[0] == "_" else -0.38), 1)
            out.append(f'<tspan dy="{d}" font-size="{round(size * .72, 1)}">{esc(p[2:-1])}</tspan>')
            shift = -d
        else:
            dy = f' dy="{shift}"' if shift else ""
            out.append(f"<tspan{dy}>{esc(p)}</tspan>")
            shift = 0
    return "".join(out)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=14, a="start", fill=INK, b=False, it=False, font=SANS):
    """Texte. a = start | middle | end."""
    svg.append(
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{a}" fill="{fill}" font-family="{font}"'
        + (' font-weight="700"' if b else "") + (' font-style="italic"' if it else "")
        + f' xml:space="preserve">{rich(s, size)}</text>'
    )


def M(x, y, s, size=15, a="start", fill=INK, b=False):
    """Texte en police mathematique (formules)."""
    T(x, y, s, size, a, fill, b, False, MATH)


def para(x, y, s, size=15, w=900, lh=None, fill=INK, b=False):
    """Paragraphe coupe a la largeur w. Renvoie le y sous le paragraphe."""
    lh = lh or size * 1.34
    cur, out = "", []
    for mot in s.split(" "):
        test = (cur + " " + mot).strip()
        if len(nu(test)) * size * 0.49 > w and cur:
            out.append(cur)
            cur = mot
        else:
            cur = test
    out.append(cur)
    for k, l_ in enumerate(out):
        T(x, y + k * lh, l_, size, "start", fill, b)
    return y + len(out) * lh


def rouge(x, y, s, size=15, a="start"):
    T(x, y, s, size, a, RED, True)


# ---------------------------------------------------------------- traits
def L(x1, y1, x2, y2, c=INK, w=1.6, dash=None, end=None, start=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    extra += f' marker-end="url(#{end})"' if end else ""
    extra += f' marker-start="url(#{start})"' if start else ""
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{extra}/>')


def poly(pts, c=INK, w=2.1, dash=None):
    d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    svg.append(f'<polyline points="{d}" fill="none" stroke="{c}" stroke-width="{w}" '
               f'stroke-linejoin="round" stroke-linecap="round"{extra}/>')


def rect(x, y, w, h, c=INK, sw=1.6, fill="#fff", rx=0):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')


def dot(x, y, r=4.5, c=RED):
    svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')


def croix(x, y, s=7, c=RED):
    L(x - s, y - s, x + s, y + s, c, 3)
    L(x - s, y + s, x + s, y - s, c, 3)


def fleche(a, b, c=RED, w=2.2):
    L(a[0], a[1], b[0], b[1], c, w, end="ars" if c == RED else "ah")


def double(xa, ya, xb, yb, w=1.9):
    """Double fleche rouge (mesure d'un ecart)."""
    L(xa, ya, xb, yb, RED, w, end="ars", start="ars")


def badge(x, y, n):
    """Pastille rouge numerotee (numeros de cables, d'etapes)."""
    svg.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{RED}"/>')
    svg.append(f'<text x="{x}" y="{y + 5}" font-size="14" font-weight="700" text-anchor="middle" '
               f'fill="#fff" stroke="none" font-family="{SANS}">{n}</text>')


def image(x, y, w, b64, size, cadre=True):
    """Image PNG en base64 ; size = (largeur, hauteur) en pixels. Renvoie la hauteur dessinee."""
    h = w * size[1] / size[0]
    svg.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{b64}"/>')
    if cadre:
        rect(x, y, w, h, LIGHT, 1, "none")
    return h


# ---------------------------------------------------------------- schemas blocs
def box(x, cy, w, h, label=None, size=15):
    rect(x, cy - h / 2, w, h)
    if label:
        M(x + w / 2, cy + size * 0.34, label, size, "middle")


def comparateur(cx, cy, r=13):
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
    k = r * 0.707
    L(cx - k, cy - k, cx + k, cy + k, INK, 1.2)
    L(cx - k, cy + k, cx + k, cy - k, INK, 1.2)
    T(cx - r + 3, cy + 4, "+", 10.5, "start", INK, True)
    T(cx, cy + r - 2.5, "–", 10.5, "middle", INK, True)


def frac(cx, cy, top, bot, size=14, width=None, c=INK):
    w = width or max(len(nu(top)), len(nu(bot))) * size * 0.5 + 4
    M(cx, cy - 4.5, top, size, "middle", c)
    L(cx - w / 2, cy, cx + w / 2, cy, c, 1.1)
    M(cx, cy + size * 0.95, bot, size, "middle", c)


# ---------------------------------------------------------------- courbes
class Plot:
    """Axes simples (t, y) ; E=True trace l'echelon jaune a 1."""

    def __init__(self, x, y, w, h, tmax, ymax=1.5, E=False, xlab="t", ylab=""):
        self.x, self.y, self.w, self.h, self.tmax, self.ymax = x, y, w, h, tmax, ymax
        L(x, y + h, x + w, y + h, INK, 1.2, end="ah")
        L(x, y + h, x, y - 4, INK, 1.2, end="ah")
        if xlab:
            T(x + w, y + h + 18, xlab, 13, "end", GREY)
        if ylab:
            T(x - 6, y - 8, ylab, 13, "end", GREY)
        if E:
            poly([(x, y + h), (x, self.Y(1)), (x + w - 8, self.Y(1))], YEL, 3)

    def X(self, t):
        return self.x + t / self.tmax * (self.w - 10)

    def Y(self, v):
        return self.y + self.h - v / self.ymax * self.h

    def curve(self, f, c=INK, w=2.1, dash=None, n=420):
        poly([(self.X(self.tmax * i / n), self.Y(f(self.tmax * i / n))) for i in range(n + 1)], c, w, dash)

    def niveau(self, v, t, lab_y="", lab_t=""):
        """Curseurs comme a l'oscillo : niveau v atteint a l'instant t."""
        L(self.X(0), self.Y(v), self.X(t), self.Y(v), RED, 1.3, "5 4")
        L(self.X(t), self.Y(v), self.X(t), self.Y(0), RED, 1.3, "5 4")
        dot(self.X(t), self.Y(v), 3.6)
        if lab_y:
            T(self.X(t) + 8, self.Y(v) + 20, lab_y, 14, "start", RED, True)
        if lab_t:
            yy = self.Y(0) + 15
            double(self.X(0), yy, self.X(t), yy)
            T(self.X(t) + 8, yy + 6, lab_t, 15, "start", RED, True)


def osc(x, y, div, titre, traces, calibres, t0=1.0, n=1100):
    """Ecran d'oscilloscope 10 x 8 div.
    traces : liste de (couleur, numero_voie, ref_en_div, f) avec f(t_div) -> y_div.
    calibres : liste de (texte, couleur), affiches a cote du titre.
    t0 : position du declenchement en div. Renvoie (X, Y) : div -> pixels, pour annoter."""
    T(x, y - 28, titre, 15.5, "start", INK, True)
    xc = x + 200
    for txt, c in calibres:
        T(xc, y - 28, txt, 14, "start", c, True)
        xc += len(txt) * 7.4 + 22
    X = lambda t: x + t * div
    Y = lambda v: y + 4 * div - v * div
    rect(x, y, 10 * div, 8 * div, INK, 1.6)
    for i in range(1, 10):
        L(X(i), y, X(i), y + 8 * div, "#cfcfcf", 0.8)
    for j in range(1, 8):
        L(x, y + j * div, x + 10 * div, y + j * div, "#cfcfcf", 0.8)
    L(X(5), y, X(5), y + 8 * div, "#8a8a8a", 1)
    L(x, Y(0), x + 10 * div, Y(0), "#8a8a8a", 1)
    for i in range(51):
        L(x + i * div / 5, Y(0) - 3.5, x + i * div / 5, Y(0) + 3.5, "#8a8a8a", 0.8)
    for j in range(41):
        L(X(5) - 3.5, y + j * div / 5, X(5) + 3.5, y + j * div / 5, "#8a8a8a", 0.8)
    px = X(t0)
    svg.append(f'<polygon points="{px - 6},{y - 1} {px + 6},{y - 1} {px},{y + 9}" fill="{INK}"/>')
    for c, num, ref, f in traces:
        ry = Y(ref)
        svg.append(f'<polygon points="{x - 13},{ry - 6} {x - 13},{ry + 6} {x - 3},{ry}" fill="{c}"/>')
        T(x - 15, ry + 5, str(num), 13, "end", c, True)
        seg = []
        for i in range(n + 1):
            t = 10 * i / n
            v = f(t)
            if -3.98 <= v <= 3.98:
                seg.append((X(t), Y(v)))
            elif seg:
                poly(seg, c, 1.7)
                seg = []
        if seg:
            poly(seg, c, 1.7)
    return X, Y


def hl(X, Y, v, ta, tb, w=1.4):
    """Niveau horizontal pointille rouge (en div), de ta a tb."""
    L(X(ta), Y(v), X(tb), Y(v), RED, w, "6 4")


def vl(X, Y, t, va, vb, w=1.4):
    """Trait vertical pointille rouge (en div)."""
    L(X(t), Y(va), X(t), Y(vb), RED, w, "6 4")


def matlab(x, y, w, h, xr, yr, xstep, ystep, titre, courbes, xfmt="{:.2f}", yfmt="{:.2f}", xlab="temps (s)"):
    """Figure facon Matlab/Simulink. courbes : (f, couleur, epaisseur). Renvoie (X, Y) pour annoter."""
    T(x + w / 2, y - 8, titre, 14, "middle", INK, True)
    X = lambda a: x + (a - xr[0]) / (xr[1] - xr[0]) * w
    Y = lambda a: y + h - (a - yr[0]) / (yr[1] - yr[0]) * h
    rect(x, y, w, h, INK, 1.4)
    nx, ny = round((xr[1] - xr[0]) / xstep), round((yr[1] - yr[0]) / ystep)
    for i in range(nx + 1):
        a = xr[0] + i * xstep
        L(X(a), y, X(a), y + h, "#d0d0d0", 0.8)
        if i % max(1, nx // 6) == 0:
            T(X(a), y + h + 16, xfmt.format(a).replace(".", ","), 12.5, "middle", INK)
    for j in range(ny + 1):
        a = yr[0] + j * ystep
        L(x, Y(a), x + w, Y(a), "#d0d0d0", 0.8)
        if j % max(1, ny // 6) == 0:
            T(x - 6, Y(a) + 4, yfmt.format(a).replace(".", ","), 12.5, "end", INK)
    T(x + w, y + h + 32, xlab, 12.5, "end", GREY)
    for f, c, wd in courbes:
        seg = []
        for i in range(901):
            a = xr[0] + (xr[1] - xr[0]) * i / 900
            v = f(a)
            if yr[0] <= v <= yr[1]:
                seg.append((X(a), Y(v)))
            else:
                if seg:
                    poly(seg, c, wd)
                seg = []
        if seg:
            poly(seg, c, wd)
    return X, Y


def s2(t, H0=1.0, z=0.5, wn=100.0):
    """Reponse indicielle d'un 2nd ordre (pour dessiner des allures)."""
    if t <= 0:
        return 0.0
    if abs(z - 1) < 1e-6:
        return H0 * (1 - math.exp(-wn * t) * (1 + wn * t))
    if z < 1:
        wd = wn * math.sqrt(1 - z * z)
        return H0 * (1 - math.exp(-z * wn * t) * (math.cos(wd * t) + z / math.sqrt(1 - z * z) * math.sin(wd * t)))
    r = math.sqrt(z * z - 1)
    p1, p2 = wn * (z - r), wn * (z + r)
    return H0 * (1 - (p2 * math.exp(-p1 * t) - p1 * math.exp(-p2 * t)) / (p2 - p1))


# ---------------------------------------------------------------- blocs de fiche
def entete(gauche, droite=""):
    T(30, 44, gauche, 24, b=True)
    if droite:
        T(970, 42, droite, 15, "end", RED, True)
    L(30, 56, 970, 56, INK, 2)


def carte(x, y, w, num, titre, pts, lignes, res=None):
    """Une question : titre, calcul, resultat encadre en rouge.
    lignes : formules (police math) ; '#texte' = note grise ; '!texte' = piege en rouge.
    res : une chaine ou une liste de chaines encadrees en rouge. Renvoie le y suivant."""
    T(x, y, num, 16.5, "start", INK, True)
    T(x + (42 if num else 0), y, titre, 15, "start", INK, True)
    if pts:
        T(x + w, y, pts, 13, "end", GREY)
    yy = y + 28
    for l_ in lignes:
        if l_.startswith("#"):
            yy = para(x + 8, yy, l_[1:].strip(), 13.5, w - 10, 19, GREY)
        elif l_.startswith("!"):
            yy = para(x + 8, yy, "Piège : " + l_[1:].strip(), 13.5, w - 10, 19, RED, True)
        else:
            M(x + 8, yy, l_, 15.5)
            yy += 23
    for r_ in ([res] if isinstance(res, str) else (res or [])):
        ww = min(w, len(nu(r_)) * 16 * 0.53 + 26)
        rect(x + 2, yy - 8, ww, 32, RED, 2.2, "#fff", 4)
        T(x + 14, yy + 14, r_, 16, "start", RED, True)
        yy += 40
    return yy + 16


def case(x, y, w, h, titre, sous=""):
    """Cadre arrondi (fiche a retenir, questions ratees). Renvoie (x, y) interieurs."""
    rect(x, y, w, h, LIGHT, 1.2, "#fff", 6)
    T(x + 14, y + 26, titre, 16.5, "start", INK, True)
    if sous:
        T(x + w - 14, y + 26, sous, 13, "end", GREY, True)
    return x + 14, y + 26


# ---------------------------------------------------------------- pages
def open_page():
    svg.clear()
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">{DEFS}'
               f'<rect width="{W}" height="{H}" fill="#fff"/>')


def fin_page():
    svg.append("</svg>")
    pages.append("".join(svg))


def ecrire(titre, out):
    """Ecrit toutes les pages dans un HTML imprimable en A4 (une page SVG = une feuille)."""
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titre)}</title>
<style>
  html, body {{ margin: 0; background: #fff; }}
  main {{ max-width: 900px; margin: 0 auto; padding: 8px; }}
  svg {{ display: block; width: 100%; height: auto; margin-bottom: 16px; }}
  @page {{ size: A4 portrait; margin: 0; }}
  @media print {{
    main {{ max-width: none; padding: 0; }}
    svg {{ width: 210mm; height: 296mm; margin: 0; break-after: page; }}
    svg:last-child {{ break-after: auto; }}
  }}
</style></head>
<body><main>{"".join(pages)}</main></body></html>
"""
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("ok", out, len(pages), "page(s)")
