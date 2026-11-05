"""Base des animations de TP (ManimGL) : voix synchronisee, parties bien separees, etapes annoncees.

Dans une scene :

    import sys; sys.path.insert(0, r"<dossier du skill>/scripts")
    from scene_base import *

    PLAN = ["Système", "Câblage", "Ordre 1", "Ordre 2", "Conclusion"]

    class TP1(SceneTP):
        nom, plan = "TP1", PLAN
        def construct(self):
            self.partie(0, "p_sys")                 # ecran noir + plan, voix "p_sys"
            self.etape("ON RAJOUTE", "le moteur")   # efface l'etape precedente
            self.speak("sys1"); self.play(FadeIn(bloc("MCC")))
            self.panel_add(tx("G0 = 0,15", 26, C_G0))   # recapitulatif qui reste a droite
            self.fin()

Rendu (video muette + timeline.json), puis voix.py mixer :
    $env:VOIX="Remy"; manimgl TP1.py TP1 -w --hd --video_dir voix/TP1/Remy --file_name muet

Les couleurs ci-dessous sont un point de depart : les remplacer par celles relevees
sur la video du prof (extraire des images avec ffmpeg et lire les couleurs des pixels).
"""
import json
import os
import pathlib

from manimlib import *

FONT = "Cambria"
# palette par defaut, fond noir (a remplacer par celle du prof)
C_U, C_M, C_OM, C_EPS = "#A44C64", "#84C46C", "#F4E4B4", "#CC4CBC"
C_H, C_G0, C_Z, C_WN = "#ECB0BC", "#F4CCA4", "#F4E4C0", "#A0E0C8"
SOFT = "#9A9A9A"
# exception : bornes et cables aux vraies couleurs du materiel
B_ROUGE, B_NOIR, B_VERT, B_JAUNE = "#E5484D", "#8A8A8A", "#4CD964", "#F4C430"


def tx(s, size=30, color=WHITE):
    return MarkupText(s, font=FONT, font_size=size).set_color(color)


def frac(top, bot, size=28, ctop=WHITE, cbot=WHITE):
    a = top if isinstance(top, Mobject) else tx(top, size, ctop)
    b = bot if isinstance(bot, Mobject) else tx(bot, size, cbot)
    bar = Line(LEFT, RIGHT, stroke_width=2, stroke_color=WHITE).set_width(max(a.get_width(), b.get_width()) + 0.12)
    return VGroup(a, bar, b).arrange(DOWN, buff=0.08)


def eq(*parts, buff=0.13):
    return VGroup(*parts).arrange(RIGHT, buff=buff)


def fleche(a, b, color=WHITE):
    return Arrow(np.array(a), np.array(b), buff=0, thickness=3.0, fill_color=color, max_width_to_length_ratio=20)


def double(a, b, color=WHITE):
    a, b = np.array(a), np.array(b)
    mid = (a + b) / 2
    return VGroup(fleche(mid, a, color), fleche(mid, b, color))


def bloc(texte, w=2.0, h=1.0, size=26, color=WHITE):
    r = Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=3)
    return VGroup(r, tx(texte, size, color).move_to(r))


def fil(points, color=WHITE, width=3):
    v = VMobject(stroke_color=color, stroke_width=width)
    v.set_points_as_corners([np.array(tuple(p) + (0,)) for p in points])
    return v


class Stage(VGroup):
    """Axes facon oscillo : path() pour des mesures, fn() pour un modele."""

    def __init__(self, xr, yr, xt, yt, ylab="Δ (V)", xlab="t (ms)", center=2.5 * LEFT + 0.05 * DOWN, width=7.9, height=4.9):
        self.ax = Axes(x_range=xr, y_range=yr, width=width, height=height,
                       axis_config=dict(stroke_color=WHITE, stroke_width=2, include_tip=True, tick_size=0.05))
        self.ax.move_to(center)
        lab = VGroup()
        for v in xt:
            lab.add(tx(f"{v:g}".replace(".", ","), 18, SOFT).next_to(self.ax.c2p(v, yr[0]), DOWN, buff=0.14))
        for v in yt:
            lab.add(tx(f"{v:g}".replace(".", ","), 18, SOFT).next_to(self.ax.c2p(xr[0], v), LEFT, buff=0.14))
        lab.add(tx(xlab, 18).next_to(self.ax.c2p(xr[1], yr[0]), RIGHT, buff=0.3))
        lab.add(tx(ylab, 18).next_to(self.ax.c2p(xr[0], yr[1]), UP, buff=0.06))
        self.xr, self.yr = xr, yr
        super().__init__(self.ax, lab)

    def path(self, ts, vs, color, width=4):
        pts = [self.ax.c2p(t, v) for t, v in zip(ts, vs)
               if self.xr[0] <= t <= self.xr[1] * 0.985 and self.yr[0] <= v <= self.yr[1]]
        c = VMobject(stroke_color=color, stroke_width=width)
        c.set_points_as_corners(pts)
        return c

    def fn(self, f, color, n=260, width=3.5):
        t1 = self.xr[1] * 0.985
        ts = [t1 * i / n for i in range(n + 1)]
        return self.path(ts, [f(t) for t in ts], color, width)


class SceneTP(Scene):
    default_camera_config = dict(background_color=BLACK)
    nom = "TP"
    plan = []

    def setup(self):
        voix = os.environ.get("VOIX", "Remy")
        self.voix_dir = pathlib.Path.cwd() / "voix" / self.nom / voix
        f = self.voix_dir / "durees.json"
        self.durees = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        self.timeline, self.voice_end = [], 0.0
        self.head, self.chip, self.panel = None, None, VGroup()

    # ---------- voix
    def sync(self, pad=0.3):
        """Attend la fin de la phrase en cours."""
        rest = self.voice_end + pad - self.get_time()
        if rest > 0.02:
            self.wait(rest)

    def speak(self, cle):
        """Lance la phrase `cle` de NARRATION ; les animations suivantes jouent pendant qu'elle parle."""
        self.sync()
        self.timeline.append((self.get_time(), cle))
        self.voice_end = self.get_time() + self.durees.get(cle, 2.0)

    def fin(self):
        self.sync(0.8)
        self.voix_dir.mkdir(parents=True, exist_ok=True)
        (self.voix_dir / "timeline.json").write_text(json.dumps(self.timeline), encoding="utf-8")

    # ---------- structure : separer vraiment les parties et les etapes
    def clear_screen(self, keep=()):
        mobs = [m for m in self.mobjects if m is not self.camera.frame and m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.4)

    def partie(self, i, cle, couleur=C_OM):
        """Ecran noir : on change de partie. Le plan s'affiche avec la partie en cours."""
        self.sync()
        self.clear_screen()
        self.head, self.chip, self.panel = None, None, VGroup()
        self.wait(0.2)
        titre = tx(self.plan[i], 62, couleur)
        items = VGroup(*[tx(p, 20, couleur if k == i else (WHITE if k < i else "#555555"))
                         for k, p in enumerate(self.plan)]).arrange(RIGHT, buff=0.42).to_edge(DOWN, buff=0.75)
        ligne = Line(items.get_left(), items.get_right(), stroke_color="#555555", stroke_width=2).next_to(items, UP, buff=0.18)
        repere = Line(items[i].get_left(), items[i].get_right(), stroke_color=couleur, stroke_width=5).move_to(
            np.array([items[i].get_center()[0], ligne.get_center()[1], 0]))
        self.speak(cle)
        self.play(Write(titre), FadeIn(items), ShowCreation(ligne), ShowCreation(repere), run_time=0.8)
        self.sync(0.5)
        self.play(FadeOut(VGroup(titre, items, ligne, repere)), run_time=0.4)
        self.head = tx(self.plan[i], 24, couleur).to_corner(UL, buff=0.28)
        self.play(FadeIn(self.head), run_time=0.3)

    def etape(self, verbe, detail="", fort=False, garder=()):
        """Chaque etape efface la precedente et s'annonce : ON RAJOUTE, ON MODIFIE, ON MESURE, ON ALLUME..."""
        self.sync()
        keep = {id(self.head)} | {id(m) for m in self.panel} | {id(g) for g in garder}
        mobs = [m for m in self.mobjects if m is not self.camera.frame and id(m) not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.35)
        t = tx(verbe, 22, BLACK if fort else WHITE)
        fond = RoundedRectangle(width=t.get_width() + 0.4, height=t.get_height() + 0.22, corner_radius=0.08,
                                stroke_color=C_EPS if fort else WHITE, stroke_width=2,
                                fill_color=C_EPS if fort else BLACK, fill_opacity=1)
        t.move_to(fond)
        chip = VGroup(fond, t)
        if self.head:
            chip.next_to(self.head, RIGHT, buff=0.35)
        else:
            chip.to_corner(UL, buff=0.28)
        d = tx(detail, 24).next_to(chip, RIGHT, buff=0.25) if detail else VGroup()
        self.chip = VGroup(chip, d)
        self.play(FadeIn(self.chip, shift=0.1 * DOWN), run_time=0.35)

    def legende(self, s, size=28):
        c = tx(s, size).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(c, shift=0.08 * UP), run_time=0.35)
        return c

    def panel_add(self, mob, buff=0.3):
        """Recapitulatif a droite : reste affiche d'une etape a l'autre de la partie."""
        if len(self.panel):
            mob.next_to(self.panel[-1], DOWN, buff=buff, aligned_edge=LEFT)
        else:
            mob.move_to(np.array([2.15, 2.75, 0]), UL)
        self.play(FadeIn(mob, shift=0.12 * LEFT), run_time=0.5)
        self.panel.add(mob)

    # ---------- curseurs de l'oscillo
    def curseur_y(self, st, v, nom):
        ax = st.ax
        l_ = DashedLine(ax.c2p(st.xr[0], v), ax.c2p(st.xr[1] * 0.985, v), stroke_color=WHITE, stroke_width=2)
        t = tx(nom, 20).next_to(ax.c2p(st.xr[1] * 0.985, v), RIGHT, buff=0.08)
        self.play(ShowCreation(l_), FadeIn(t), run_time=0.6)
        return VGroup(l_, t)

    def curseur_t(self, st, t, v, nom_y, nom_x):
        """Curseur Y au niveau v, curseur X a l'instant t, et l'ecart X1-X2 sous l'axe."""
        ax = st.ax
        h = DashedLine(ax.c2p(st.xr[0], v), ax.c2p(t, v), stroke_color=WHITE, stroke_width=2)
        ly = tx(nom_y, 20).next_to(ax.c2p(t, v), RIGHT, buff=0.16).shift(0.2 * DOWN)
        self.play(ShowCreation(h), FadeIn(ly), run_time=0.7)
        d0 = Dot(ax.c2p(t, v), radius=0.07, fill_color=WHITE)
        x2 = DashedLine(ax.c2p(t, st.yr[1]), ax.c2p(t, st.yr[0]), stroke_color=WHITE, stroke_width=2)
        self.play(FadeIn(d0, scale=2), ShowCreation(x2), run_time=0.7)
        p0, p1 = ax.c2p(0, st.yr[0]) + 0.62 * DOWN, ax.c2p(t, st.yr[0]) + 0.62 * DOWN
        dd = double(p0, p1)
        lab = tx(nom_x, 24).next_to(p1, RIGHT, buff=0.15)
        self.play(FadeIn(dd), FadeIn(lab), run_time=0.5)
        return VGroup(h, ly, d0, x2, dd, lab)
