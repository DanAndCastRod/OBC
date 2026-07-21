#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenera los 7 GIFs didacticos de la presentacion de sustentacion.

Salida (sobrescribe en docs/presentacion/figuras/):
    intuicion_ga.gif, intuicion_sa.gif, intuicion_de.gif, intuicion_ga_sa.gif,
    chromosome_build.gif, neighborhood_operators.gif, exploration_exploitation.gif

Reproducible: todas las simulaciones usan semillas fijas (np.random.default_rng).
Lenguaje visual: tema "tinta institucional" de la presentacion (fondo #FAFAF7,
texto tinta #17202A, acentos Okabe-Ito por algoritmo), lienzo 800x450 @ 10 fps.

Uso:
    python build_intuition_gifs.py [--only ga,sa,...] [--contact-sheets DIR]
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

# --------------------------------------------------------------------------- tema
BG, INK, SEC, GRID = "#FAFAF7", "#17202A", "#5C6670", "#D9DCD6"
C_GA, C_SA, C_DE, C_HY = "#0072B2", "#E69F00", "#009E73", "#CC79A7"
C_STAR, NAVY = "#9B1B30", "#1E3A5F"
C_OK, C_BAD = "#1B7837", "#9B1B30"
F_MS, HOLD_MS = 100, 1000          # 10 fps; sostener inicio/fin ~1 s
MAX_BYTES = 400_000
LAND_RECT = (0.075, 0.115, 0.85, 0.585)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "dejavusans",
    "axes.unicode_minus": False,
})

OUTDIR = Path(__file__).resolve().parents[1] / "figuras"

# ---------------------------------------------------------------- paisaje comun
PEAKS = [(1.3, 0.60, 0.55), (3.2, 0.78, 0.65), (5.0, 0.50, 0.45),
         (6.6, 1.00, 0.55), (8.7, 0.68, 0.70)]


def f(x):
    x = np.asarray(x, dtype=float)
    y = 0.06 + 0.03 * np.sin(1.7 * x)
    for c, a, w in PEAKS:
        y = y + a * np.exp(-(((x - c) / w) ** 2))
    return y


XS = np.linspace(0.0, 10.0, 1200)
YS = f(XS)
X_STAR = float(XS[np.argmax(YS)])
Y_STAR = float(YS.max())


def ease(t):
    t = min(1.0, max(0.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def lerp(a, b, t):
    return a + (b - a) * t


# ----------------------------------------------------------- infraestructura GIF
def snap(fig):
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba(), dtype=np.uint8)[..., :3].copy()
    plt.close(fig)
    return Image.fromarray(buf)


class GifWriter:
    def __init__(self):
        self.frames, self.durs = [], []

    def add(self, fig, ms=F_MS):
        self.frames.append(snap(fig))
        self.durs.append(int(ms))

    def hold(self, ms):
        self.durs[-1] += int(ms)


def write_gif(path: Path, w: GifWriter, colors=128):
    idx = np.linspace(0, len(w.frames) - 1, min(12, len(w.frames))).astype(int)
    thumbs = [w.frames[i].resize((w.frames[i].width // 2, w.frames[i].height // 2))
              for i in idx]
    mosaic = Image.new("RGB", (thumbs[0].width, thumbs[0].height * len(thumbs)))
    for j, t in enumerate(thumbs):
        mosaic.paste(t, (0, j * t.height))
    size = None
    for c in (colors, 96, 64):
        master = mosaic.quantize(colors=c, method=Image.MEDIANCUT)
        q = [fr.quantize(colors=c, palette=master, dither=Image.Dither.NONE)
             for fr in w.frames]
        q[0].save(path, save_all=True, append_images=q[1:], duration=w.durs,
                  loop=0, optimize=True)
        size = path.stat().st_size
        if size <= MAX_BYTES:
            break
    return size


# --------------------------------------------------------------- lienzo y header
def new_fig():
    fig = plt.figure(figsize=(8, 4.5), dpi=100)
    fig.patch.set_facecolor(BG)
    return fig


def header(fig, title, subtitle="", counter=""):
    fig.text(0.045, 0.955, title, fontsize=15, fontweight="bold",
             color=INK, va="top", ha="left")
    if subtitle:
        fig.text(0.045, 0.885, subtitle, fontsize=12, color=SEC,
                 va="top", ha="left")
    if counter:
        fig.text(0.955, 0.955, counter, fontsize=11, color=SEC,
                 va="top", ha="right")


def landscape_axes(fig, rect=LAND_RECT):
    ax = fig.add_axes(rect)
    ax.set_facecolor(BG)
    for gy in (0.25, 0.50, 0.75, 1.00, 1.25):
        ax.axhline(gy, color=GRID, lw=0.7, zorder=0)
    ax.fill_between(XS, YS, 0, color=GRID, alpha=0.30, zorder=1)
    ax.plot(XS, YS, color=SEC, lw=1.6, zorder=3)
    ax.scatter([X_STAR], [Y_STAR + 0.06], marker="*", s=140, color=C_STAR,
               zorder=7, edgecolors="none")
    ax.text(X_STAR + 0.22, Y_STAR + 0.055, "óptimo", fontsize=9.5, color=SEC,
            ha="left", va="center", zorder=7)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.38)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.set_xlabel("espacio de soluciones", fontsize=10, color=SEC)
    ax.set_ylabel("fitness", fontsize=10, color=SEC)
    return ax


def pixel_axes(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 450)
    ax.axis("off")
    ax.set_facecolor(BG)
    return ax


def rrect(ax, x, y, w, h, r=6, fc="none", ec=INK, lw=1.2, alpha=1.0, zorder=3):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha,
                       zorder=zorder)
    ax.add_patch(p)
    return p


def arrow(ax, xa, ya, xb, yb, color, lw=1.6, rad=0.0, alpha=1.0, ms=11,
          ls="-", zorder=6, style="-|>"):
    p = FancyArrowPatch((xa, ya), (xb, yb), arrowstyle=style, mutation_scale=ms,
                        connectionstyle=f"arc3,rad={rad}", color=color, lw=lw,
                        alpha=alpha, linestyle=ls, zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(p)
    return p


def curve_path(xa, xb, n=28):
    xs = np.linspace(xa, xb, n)
    return xs, f(xs)


def bezier(p0, p1, p2, n=30):
    t = np.linspace(0, 1, n)[:, None]
    pts = ((1 - t) ** 2) * np.array(p0) + 2 * (1 - t) * t * np.array(p1) \
        + (t ** 2) * np.array(p2)
    return pts[:, 0], pts[:, 1]


def lupa(ax, x, y, color=C_SA):
    """Anillo de lupa con mango sobre un punto (coords de datos)."""
    ax.scatter([x], [y], s=560, facecolors="none", edgecolors=color,
               linewidths=2.0, zorder=8)
    p0 = ax.transData.transform((x, y))
    a, b = ax.transData.inverted().transform([(p0[0] + 10, p0[1] - 10),
                                              (p0[0] + 21, p0[1] - 21)])
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=2.4,
            solid_capstyle="round", zorder=8)


# =========================================================================== GA
GA_TITLE = "Algoritmo Genético (GA)"


def sim_ga(seed=7, gens=6, n=10, keep=5):
    rng = np.random.default_rng(seed)
    pop = rng.uniform(0.4, 9.6, n)
    hist = []
    for g in range(gens):
        fit = f(pop)
        order = np.argsort(-fit)
        surv = pop[order[:keep]]
        sigma = 0.55 * (0.30 ** (g / (gens - 1)))
        kids = []
        for _ in range(n - keep):
            p1, p2 = rng.choice(surv, 2, replace=False)
            u = rng.uniform(0.25, 0.75)
            pre = u * p1 + (1 - u) * p2
            post = float(np.clip(pre + rng.normal(0, sigma), 0.2, 9.8))
            kids.append((float(p1), float(p2), float(pre), post))
        hist.append(dict(pop=pop.copy(), fit=fit, surv=order[:keep],
                         doom=order[keep:], kids=kids))
        pop = np.concatenate([surv, [k[3] for k in kids]])
    return hist, pop


def _ga_scatter(ax, xs_pts, sizes, alphas, color):
    for x, s, a in zip(xs_pts, sizes, alphas):
        ax.scatter([x], [f(x)], s=s, color=color, alpha=a,
                   edgecolors=INK, linewidths=0.7, zorder=6)


def _ga_generation(wtr, st, g, gens, color, title, phase_lens,
                   sa_extra=None, label_ga=""):
    """Anima una generacion GA (evaluacion/seleccion/cruce/mutacion)."""
    pop, fit = st["pop"], st["fit"]
    surv, doom, kids = st["surv"], st["doom"], st["kids"]
    fn = (fit - fit.min()) / (np.ptp(fit) + 1e-9)
    cnt = f"generación {g + 1}/{gens}"
    n_ev, n_se, n_cr, n_mu = phase_lens
    pre_t = f"{label_ga}: " if label_ga else ""

    def base_sizes(t_eval=1.0):
        return [lerp(42, 30 + 175 * fn[i] ** 1.25, t_eval) for i in range(len(pop))]

    # --- evaluacion
    for k in range(n_ev):
        t = ease((k + 1) / n_ev)
        fig = new_fig()
        header(fig, title, pre_t + "evaluación — el tamaño refleja el fitness", cnt)
        ax = landscape_axes(fig)
        _ga_scatter(ax, pop, base_sizes(t), [0.95] * len(pop), color)
        wtr.add(fig)
    # --- seleccion
    for k in range(n_se):
        t = ease((k + 1) / n_se)
        fig = new_fig()
        header(fig, title, pre_t + "selección — sobreviven los mejores", cnt)
        ax = landscape_axes(fig)
        alphas = [0.95 if i in surv else lerp(0.9, 0.12, t) for i in range(len(pop))]
        _ga_scatter(ax, pop, base_sizes(), alphas, color)
        wtr.add(fig)
    # --- cruce
    for k in range(n_cr):
        t = ease((k + 1) / n_cr)
        fig = new_fig()
        header(fig, title, pre_t + "cruce — los hijos combinan a los padres", cnt)
        ax = landscape_axes(fig)
        alphas = [0.95 if i in surv else 0.12 for i in range(len(pop))]
        _ga_scatter(ax, pop, base_sizes(), alphas, color)
        for p1, p2, pre, _post in kids:
            apex = (0.5 * (p1 + p2), min(max(f(p1), f(p2)) + 0.25, 1.31))
            bx, by = bezier((p1, f(p1) + 0.02), apex, (p2, f(p2) + 0.02))
            ax.plot(bx, by, ls=(0, (4, 3)), lw=1.1, color=color,
                    alpha=0.55 * t, zorder=4)
            ax.scatter([pre], [f(pre)], s=52, color=color, alpha=0.9 * t,
                       edgecolors=INK, linewidths=0.7, zorder=6)
        wtr.add(fig)
    # --- mutacion
    for k in range(n_mu):
        t = ease((k + 1) / n_mu)
        fig = new_fig()
        header(fig, title, pre_t + "mutación — pequeñas variaciones aleatorias", cnt)
        ax = landscape_axes(fig)
        alphas = [0.95 if i in surv else 0.10 for i in range(len(pop))]
        _ga_scatter(ax, pop, base_sizes(), alphas, color)
        for _p1, _p2, pre, post in kids:
            xk = lerp(pre, post, t)
            ax.scatter([xk], [f(xk)], s=56, color=color, alpha=0.95,
                       edgecolors=INK, linewidths=0.7, zorder=6)
            if k < 2:  # destello breve
                ax.scatter([xk], [f(xk)], s=lerp(220, 460, k / 1.0),
                           facecolors="none", edgecolors=color,
                           linewidths=1.4, alpha=0.5 - 0.25 * k, zorder=5)
        if sa_extra is not None:
            sa_extra(ax, 1.0)
        wtr.add(fig)


def build_ga():
    hist, pop_final = sim_ga()
    wtr = GifWriter()
    # intro
    fig = new_fig()
    header(fig, GA_TITLE, "una población explora el paisaje de fitness",
           "generación 1/6")
    ax = landscape_axes(fig)
    _ga_scatter(ax, hist[0]["pop"], [42] * 10, [0.95] * 10, C_GA)
    wtr.add(fig, HOLD_MS)
    for g, st in enumerate(hist):
        _ga_generation(wtr, st, g, 6, C_GA, GA_TITLE, (4, 3, 5, 4))
    # cierre
    fig = new_fig()
    header(fig, GA_TITLE, "la población converge al óptimo global",
           "generación 6/6")
    ax = landscape_axes(fig)
    _ga_scatter(ax, pop_final, [60] * 10, [0.95] * 10, C_GA)
    wtr.add(fig, HOLD_MS + 200)
    return wtr


# =========================================================================== SA
SA_TITLE = "Recocido Simulado (SA)"
#            (propuesta, tipo)   tipo: up / worse_acc / worse_rej / reheat
SA_MOVES = [(1.32, "up"), (2.15, "worse_acc"), (3.05, "up"), (3.22, "up"),
            (4.25, "worse_acc"), (4.98, "up"), (5.55, "worse_rej"),
            (None, "reheat"), (5.75, "worse_acc"), (6.35, "up"), (6.58, "up"),
            (7.05, "worse_rej"), (6.61, "up")]
SA_TEMPS = [0.95, 0.82, 0.70, 0.60, 0.50, 0.40, 0.24, 0.60, 0.55, 0.44,
            0.33, 0.16, 0.10]
SA_X0 = 1.00
SA_SUBT = {"up": "cuesta arriba — siempre se acepta",
           "worse_acc": "acepta peor — T alta: explora",
           "worse_rej": "rechaza peor — T baja: explota",
           "reheat": "reheat — T sube para escapar del estancamiento"}

CMAP_TEMP = LinearSegmentedColormap.from_list(
    "temp", ["#2E5FA3", "#E9B25C", "#C0392B"])


def verify_sa():
    x = SA_X0
    for prop, kind in SA_MOVES:
        if kind == "reheat":
            continue
        d = float(f(prop) - f(x))
        want_up = kind == "up"
        if want_up != (d > 0):
            raise AssertionError(f"SA move {x:.2f}->{prop:.2f} tipo {kind} "
                                 f"pero df={d:+.3f}")
        if kind in ("up", "worse_acc"):
            x = prop
    if abs(x - X_STAR) > 0.15:
        raise AssertionError(f"SA no termina cerca del óptimo: x={x:.2f}")


def thermo(fig, level, reheat=False):
    ax = fig.add_axes([0.885, 0.13, 0.05, 0.56])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.axis("off")
    level = min(1.0, max(0.04, level))
    n = max(2, int(220 * level))
    grad = np.linspace(0, level, n).reshape(-1, 1)
    ax.imshow(grad, extent=(0.28, 0.72, 0, level), origin="lower",
              aspect="auto", cmap=CMAP_TEMP, vmin=0, vmax=1, zorder=2)
    rrect(ax, 0.28, 0.0, 0.44, 1.0, r=0.05, ec=SEC, lw=1.2, zorder=3)
    ax.plot([0.20, 0.80], [level, level], color=INK, lw=1.4, zorder=4)
    if reheat:
        ax.text(0.90, level, "↑", fontsize=14, color="#C0392B",
                ha="left", va="center", fontweight="bold")
    fig.text(0.910, 0.735, "T", fontsize=11, color=INK, ha="center",
             fontweight="bold")


def sa_frame(subtitle, cnt, x_cur, trail, T, reheat=False,
             ghost=None, verdict=None):
    fig = new_fig()
    header(fig, SA_TITLE, subtitle, cnt)
    ax = landscape_axes(fig, rect=(0.07, 0.115, 0.775, 0.585))
    # estela que se desvanece
    m = len(trail)
    for j, (xa, xb) in enumerate(trail[-6:]):
        age = (len(trail[-6:]) - j) / 6.0
        cx, cy = curve_path(xa, xb)
        ax.plot(cx, cy, color=C_SA, lw=2.6, alpha=max(0.08, 0.5 - 0.4 * age),
                zorder=2, solid_capstyle="round")
    if ghost is not None:
        gx, galpha = ghost
        ax.scatter([gx], [f(gx)], s=95, color=C_SA, alpha=0.40 * galpha,
                   edgecolors=INK, linewidths=0.6, zorder=5)
        rad = -0.25 if gx > x_cur else 0.25
        arrow(ax, x_cur, f(x_cur) + 0.03, gx, f(gx) + 0.03, SEC, lw=1.3,
              rad=rad, alpha=0.8 * galpha, zorder=5)
    if verdict is not None:
        vx, kind = verdict
        sym, col = ("✓", C_OK) if kind != "worse_rej" else ("✗", C_BAD)
        vy = min(max(f(vx), f(x_cur)) + 0.20, 1.30)
        ax.text(0.5 * (vx + x_cur), vy, sym, fontsize=17, color=col,
                ha="center", va="center", fontweight="bold", zorder=9)
    ax.scatter([x_cur], [f(x_cur)], s=110, color=C_SA, alpha=0.98,
               edgecolors=INK, linewidths=0.9, zorder=7)
    thermo(fig, T, reheat=reheat)
    return fig


def build_sa():
    verify_sa()
    wtr = GifWriter()
    x = SA_X0
    trail = []
    fig = sa_frame("un caminante propone vecinos aleatorios", "iteración 0",
                   x, trail, SA_TEMPS[0])
    wtr.add(fig, HOLD_MS)
    it = 0
    for (prop, kind), T in zip(SA_MOVES, SA_TEMPS):
        if kind == "reheat":
            # la barra sube gradualmente, sin movimiento del caminante
            T0 = SA_TEMPS[6]
            for k in range(5):
                t = ease((k + 1) / 5)
                fig = sa_frame(SA_SUBT[kind], f"iteración {it}", x, trail,
                               lerp(T0, T, t), reheat=True)
                wtr.add(fig)
            wtr.hold(250)
            continue
        it += 1
        cnt = f"iteración {it}"
        # propuesta (fantasma + flecha)
        for k in range(3):
            t = ease((k + 1) / 3)
            fig = sa_frame("propuesta de vecino", cnt, x, trail, T,
                           ghost=(prop, t))
            wtr.add(fig)
        # veredicto
        fig = sa_frame(SA_SUBT[kind], cnt, x, trail, T, ghost=(prop, 1.0),
                       verdict=(prop, kind))
        wtr.add(fig, 300)
        if kind in ("up", "worse_acc"):
            for k in range(4):
                t = ease((k + 1) / 4)
                xk = lerp(x, prop, t)
                tr = trail + [(x, xk)]
                fig = sa_frame(SA_SUBT[kind], cnt, xk, tr, T)
                wtr.add(fig)
            trail.append((x, prop))
            x = prop
        else:
            for k in range(2):
                t = 1.0 - ease((k + 1) / 2)
                fig = sa_frame(SA_SUBT[kind], cnt, x, trail, T,
                               ghost=(prop, t))
                wtr.add(fig)
    fig = sa_frame("termina cerca del óptimo global", f"iteración {it}",
                   x, trail, SA_TEMPS[-1])
    wtr.add(fig, HOLD_MS + 200)
    return wtr


# =========================================================================== DE
DE_TITLE = "Evolución Diferencial (DE)"
DE_F = 0.7
DE_LANE1, DE_LANE2 = 1.26, 1.14
#           r1  r2  target  resultado esperado
DE_CYCLES = [dict(r1=7, r2=3, tgt=0, expect="win"),
             dict(r1=1, r2=2, tgt=6, expect="lose"),
             dict(r1=3, r2=4, tgt=5, expect="win")]


def de_pop0():
    rng = np.random.default_rng(2)
    return np.sort(rng.uniform(0.6, 9.4, 8))


def verify_de():
    pop = de_pop0().copy()
    for c, cy in enumerate(DE_CYCLES):
        b = int(np.argmax(f(pop)))
        v = float(np.clip(pop[b] + DE_F * (pop[cy["r1"]] - pop[cy["r2"]]),
                          0.2, 9.8))
        win = f(v) > f(pop[cy["tgt"]])
        if win != (cy["expect"] == "win"):
            raise AssertionError(f"DE ciclo {c + 1}: esperado {cy['expect']}")
        if win:
            pop[cy["tgt"]] = v
    if abs(pop[np.argmax(f(pop))] - X_STAR) > 0.2:
        raise AssertionError("DE no acaba con best cerca del óptimo")


def de_frame(subtitle, cnt, pop, best=None, r1=None, r2=None, marks=None):
    """marks: lista de callables extra que dibujan sobre ax."""
    fig = new_fig()
    header(fig, DE_TITLE, subtitle, cnt)
    ax = landscape_axes(fig)
    for i, xp in enumerate(pop):
        ax.scatter([xp], [f(xp)], s=60, color=C_DE, alpha=0.95,
                   edgecolors=INK, linewidths=0.7, zorder=6)
    if best is not None:
        xb = pop[best]
        ax.scatter([xb], [f(xb)], s=300, facecolors="none", edgecolors=INK,
                   linewidths=1.6, zorder=7)
        if abs(xb - X_STAR) < 0.9:  # evita chocar con la estrella "óptimo"
            ax.text(xb - 0.38, f(xb) - 0.10, "best", fontsize=9, color=INK,
                    ha="right", fontweight="bold", zorder=8)
        else:
            ax.text(xb, min(f(xb) + 0.13, 1.32), "best", fontsize=9, color=INK,
                    ha="center", fontweight="bold", zorder=8)
    for idx, lab in ((r1, "r1"), (r2, "r2")):
        if idx is not None:
            xr = pop[idx]
            ax.scatter([xr], [f(xr)], s=240, facecolors="none",
                       edgecolors=SEC, linewidths=1.4, zorder=7)
            ax.text(xr, max(f(xr) - 0.15, 0.05), lab, fontsize=9, color=INK,
                    ha="center", zorder=8)
    if marks:
        for mk in marks:
            mk(ax)
    return fig


def build_de():
    verify_de()
    wtr = GifWriter()
    pop = de_pop0().copy()
    fig = de_frame("una población de vectores dispersa", "ciclo 1/3", pop)
    wtr.add(fig, HOLD_MS)
    for c, cy in enumerate(DE_CYCLES):
        cnt = f"ciclo {c + 1}/3"
        b = int(np.argmax(f(pop)))
        xb, x1, x2, xt = pop[b], pop[cy["r1"]], pop[cy["r2"]], pop[cy["tgt"]]
        v = float(np.clip(xb + DE_F * (x1 - x2), 0.2, 9.8))
        win = cy["expect"] == "win"
        # s1: elegir best, r1, r2
        for k in range(5):
            fig = de_frame("se eligen best, r1 y r2", cnt, pop, best=b,
                           r1=cy["r1"], r2=cy["r2"])
            wtr.add(fig)
        # s2: vector diferencia en carril superior
        for k in range(6):
            t = ease((k + 1) / 6)

            def mk(ax, t=t):
                for xr in (x1, x2):
                    ax.plot([xr, xr], [f(xr), DE_LANE1], ls=(0, (3, 3)),
                            color=SEC, lw=0.9, alpha=0.55, zorder=4)
                xe = lerp(x2, x1, t)
                arrow(ax, x2, DE_LANE1, xe, DE_LANE1, C_DE, lw=2.0, zorder=6)
                if t > 0.85:
                    ax.text(0.5 * (x1 + x2), DE_LANE1 + 0.055, "r1 − r2",
                            fontsize=9, color=INK, ha="center", zorder=8)
            fig = de_frame("diferencia de vectores", cnt, pop, best=b,
                           r1=cy["r1"], r2=cy["r2"], marks=[mk])
            wtr.add(fig)
        # s3: mutante = best + F*(r1-r2)
        for k in range(7):
            t = ease((k + 1) / 7)

            def mk(ax, t=t):
                ax.plot([x1, x1], [f(x1), DE_LANE1], ls=(0, (3, 3)), color=SEC,
                        lw=0.9, alpha=0.35, zorder=4)
                ax.plot([x2, x2], [f(x2), DE_LANE1], ls=(0, (3, 3)), color=SEC,
                        lw=0.9, alpha=0.35, zorder=4)
                arrow(ax, x2, DE_LANE1, x1, DE_LANE1, C_DE, lw=1.6,
                      alpha=0.45, zorder=5)
                ta = min(1.0, t / 0.55)
                xe = lerp(xb, v, ta)
                ax.plot([xb, xb], [f(xb), DE_LANE2], ls=(0, (3, 3)), color=SEC,
                        lw=0.9, alpha=0.55, zorder=4)
                arrow(ax, xb, DE_LANE2, xe, DE_LANE2, C_DE, lw=2.0, zorder=6)
                ax.text(0.5 * (xb + v), DE_LANE2 + 0.055, "F·(r1 − r2)",
                        fontsize=9, color=INK, ha="center", zorder=8)
                if t > 0.55:  # el mutante desciende al paisaje
                    td = (t - 0.55) / 0.45
                    yv = lerp(DE_LANE2, float(f(v)), ease(td))
                    ax.scatter([v], [yv], s=85, marker="D", color=C_DE,
                               edgecolors=INK, linewidths=0.8, zorder=7)
            fig = de_frame("mutante  v = best + F·(r1 − r2)", cnt, pop, best=b,
                           r1=cy["r1"], r2=cy["r2"], marks=[mk])
            wtr.add(fig)
        # s4: trial vs target (greedy)
        verd = "mejora ✓  reemplaza" if win else "no mejora ✗  se descarta"
        for k in range(6):
            show_fade = win and k >= 4
            t_fade = ease((k - 3) / 2) if show_fade else 0.0

            def mk(ax, k=k, t_fade=t_fade):
                ax.scatter([v], [f(v)], s=85, marker="D", color=C_DE,
                           edgecolors=INK, linewidths=0.8, zorder=7,
                           alpha=1.0 if win else 1.0 - 0.8 * ease(max(0, k - 3) / 2))
                ax.scatter([xt], [f(xt)], s=240, facecolors="none",
                           edgecolors=C_BAD, linewidths=1.4, zorder=7,
                           alpha=1.0 - 0.8 * t_fade)
                ax.text(xt, max(f(xt) - 0.15, 0.05), "target", fontsize=9,
                        color=INK, ha="center", zorder=8,
                        alpha=1.0 - t_fade)
                if k >= 2:
                    col = C_OK if win else C_BAD
                    winner = v if win else xt
                    ax.scatter([winner], [f(winner)], s=lerp(300, 480, (k - 2) / 3),
                               facecolors="none", edgecolors=col,
                               linewidths=1.6, alpha=0.75, zorder=8)
                    ax.text(min(v, 9.0), max(f(v) - 0.22, 0.07), verd,
                            fontsize=9.5, color=col, ha="center",
                            fontweight="bold", zorder=9)
            fig = de_frame("cruce y selección greedy", cnt, pop, best=b,
                           marks=[mk])
            wtr.add(fig)
        wtr.hold(250)
        if win:
            pop[cy["tgt"]] = v
        # settle
        for k in range(3):
            fig = de_frame("población actualizada", cnt, pop,
                           best=int(np.argmax(f(pop))))
            wtr.add(fig)
    fig = de_frame("la población se concentra en el óptimo", "ciclo 3/3", pop,
                   best=int(np.argmax(f(pop))))
    wtr.add(fig, HOLD_MS + 200)
    return wtr


# ======================================================================== GA-SA
HY_TITLE = "Híbrido GA-SA"


def sim_hybrid(seed=10, gens=4, n=10, keep=5):
    rng = np.random.default_rng(seed)
    pop = rng.uniform(0.4, 9.6, n)
    hist = []
    for g in range(gens):
        fit = f(pop)
        order = np.argsort(-fit)
        surv = pop[order[:keep]].copy()
        rec = dict(kind="ga" if g % 2 == 0 else "sa", pop=pop.copy(), fit=fit,
                   surv=order[:keep], doom=order[keep:], sa_paths=[])
        if rec["kind"] == "sa":
            for e in range(2):
                xw = float(surv[e])
                path = [xw]
                for _ in range(4):
                    d = float(f(xw + 1e-3) - f(xw - 1e-3))
                    xw = float(np.clip(xw + 0.18 * np.sign(d), 0.2, 9.8))
                    path.append(xw)
                surv[e] = xw
                rec["sa_paths"].append(path)
        sigma = 0.5 * (0.25 ** (g / (gens - 1)))
        kids = []
        for _ in range(n - keep):
            p1, p2 = rng.choice(surv[:3], 2, replace=False)
            u = rng.uniform(0.25, 0.75)
            pre = u * p1 + (1 - u) * p2
            post = float(np.clip(pre + rng.normal(0, sigma), 0.2, 9.8))
            kids.append((float(p1), float(p2), float(pre), post))
        rec["kids"] = kids
        hist.append(rec)
        pop = np.concatenate([surv, [k[3] for k in kids]])
    return hist, pop


def build_gasa():
    hist, pop_final = sim_hybrid()
    if abs(pop_final[np.argmax(f(pop_final))] - X_STAR) > 0.3:
        raise AssertionError("GA-SA no converge al óptimo con la semilla fijada")
    wtr = GifWriter()
    fig = new_fig()
    header(fig, HY_TITLE, "GA global + SA local sobre las élites",
           "generación 1/4")
    ax = landscape_axes(fig)
    _ga_scatter(ax, hist[0]["pop"], [42] * 10, [0.95] * 10, C_HY)
    wtr.add(fig, HOLD_MS)
    for g, st in enumerate(hist):
        cnt = f"generación {g + 1}/4"
        if st["kind"] == "ga":
            _ga_generation(wtr, st, g, 4, C_HY, HY_TITLE, (4, 3, 5, 4),
                           label_ga="fase global GA")
        else:
            pop = st["pop"]
            surv, doom = st["surv"], st["doom"]
            elites = [pop[surv[0]], pop[surv[1]]]
            paths = st["sa_paths"]
            # anillo de lupa sobre las 2 élites
            for k in range(3):
                t = ease((k + 1) / 3)
                fig = new_fig()
                header(fig, HY_TITLE,
                       "explotación local SA — se enfoca en las élites", cnt)
                ax = landscape_axes(fig)
                alphas = [0.95 if i in surv else 0.25 for i in range(len(pop))]
                _ga_scatter(ax, pop, [46] * len(pop), alphas, C_HY)
                for xe in elites:
                    lupa(ax, xe, float(f(xe)))
                wtr.add(fig)
            # pasos cortos cuesta arriba con mini-estela SA
            steps = len(paths[0]) - 1
            for sstep in range(steps):
                for sub in range(4):
                    t = ease((sub + 1) / 4)
                    fig = new_fig()
                    header(fig, HY_TITLE,
                           "explotación local SA — pasos cortos cuesta arriba",
                           cnt)
                    ax = landscape_axes(fig)
                    alphas = [0.95 if i in surv else 0.20
                              for i in range(len(pop))]
                    others = [pop[i] for i in range(len(pop))
                              if i not in (surv[0], surv[1])]
                    _ga_scatter(ax, others, [46] * len(others),
                                [0.5] * len(others), C_HY)
                    for path in paths:
                        for j in range(sstep):  # estela recorrida
                            cx, cy = curve_path(path[j], path[j + 1])
                            ax.plot(cx, cy, color=C_SA, lw=2.8, alpha=0.75,
                                    zorder=4, solid_capstyle="round")
                        xk = lerp(path[sstep], path[sstep + 1], t)
                        cx, cy = curve_path(path[sstep], xk)
                        ax.plot(cx, cy, color=C_SA, lw=2.8, alpha=0.75,
                                zorder=4, solid_capstyle="round")
                        ax.scatter([xk], [f(xk)], s=80, color=C_HY,
                                   edgecolors=C_SA, linewidths=1.6, zorder=7)
                    wtr.add(fig)
            # cruce rapido con las elites mejoradas
            for k in range(4):
                t = ease((k + 1) / 4)
                fig = new_fig()
                header(fig, HY_TITLE,
                       "las élites refinadas guían el siguiente cruce", cnt)
                ax = landscape_axes(fig)
                surv_x = [paths[0][-1], paths[1][-1]] + \
                    [pop[i] for i in surv[2:]]
                _ga_scatter(ax, surv_x, [50] * len(surv_x),
                            [0.95] * len(surv_x), C_HY)
                for _p1, _p2, pre, post in st["kids"]:
                    xk = lerp(pre, post, t)
                    ax.scatter([xk], [f(xk)], s=52, color=C_HY,
                               alpha=0.9 * t, edgecolors=INK,
                               linewidths=0.7, zorder=6)
                wtr.add(fig)
    fig = new_fig()
    header(fig, HY_TITLE, "el híbrido converge en menos generaciones (4 vs 6)",
           "generación 4/4")
    ax = landscape_axes(fig)
    _ga_scatter(ax, pop_final, [60] * 10, [0.95] * 10, C_HY)
    wtr.add(fig, HOLD_MS + 200)
    return wtr


# ================================================================== cromosoma
CH_TITLE = "Cromosoma (y, q) — 6 periodos"
CH_Y = [1, 0, 1, 1, 0, 1]
CH_Q = [180, 0, 240, 150, 0, 210]
QMIN, QMAX = 120, 260
COL_W = 78
COL_X0 = 190
ROW_H = {"hdr": (318, 34), "y": (246, 64), "q": (174, 64)}


def ch_cell(ax, i, row, text="", fc="none", tc=INK, bold=False, fs=13,
            ec=GRID, lw=1.2, alpha_fc=1.0):
    y0, h = ROW_H[row]
    x0 = COL_X0 + i * COL_W
    ax.add_patch(Rectangle((x0 + 2, y0), COL_W - 4, h, facecolor=fc,
                           edgecolor=ec, linewidth=lw, zorder=3,
                           alpha=alpha_fc if fc != "none" else 1.0))
    if text != "":
        ax.text(x0 + COL_W / 2, y0 + h / 2, text, fontsize=fs, color=tc,
                ha="center", va="center", zorder=5,
                fontweight="bold" if bold else "normal")


def ch_frame(subtitle, cnt, state, hi_col=None, rules=(0.0, 0.0),
             closing=0.0):
    """state: lista por columna de dicts {y:str|None, q:str|None, y_set, q_set}"""
    fig = new_fig()
    header(fig, CH_TITLE, subtitle, cnt)
    ax = pixel_axes(fig)
    ax.text(COL_X0 - 14, ROW_H["hdr"][0] + 17, "t =", fontsize=10.5,
            color=SEC, ha="right", va="center")
    ax.text(COL_X0 - 14, ROW_H["y"][0] + 32, r"$y_t$", fontsize=13,
            color=INK, ha="right", va="center")
    ax.text(COL_X0 - 14, ROW_H["q"][0] + 32, r"$q_t$", fontsize=13,
            color=INK, ha="right", va="center")
    for i in range(6):
        ch_cell(ax, i, "hdr", str(i + 1), tc=SEC, fs=10.5)
        st = state[i]
        # fila y
        if st["y"] is None:
            ch_cell(ax, i, "y")
        elif st["y_set"]:
            if st["y"] == "1":
                ch_cell(ax, i, "y", "1", fc=NAVY, alpha_fc=0.13, tc=NAVY,
                        bold=True, fs=15)
            else:
                ch_cell(ax, i, "y", "0", fc=GRID, alpha_fc=0.45, tc=SEC,
                        bold=True, fs=15)
        else:
            ch_cell(ax, i, "y", st["y"], tc=SEC, fs=15)
        # fila q
        if st["q"] is None:
            ch_cell(ax, i, "q")
        elif st["q_set"]:
            if st["q"] == "0":
                ch_cell(ax, i, "q", "0", fc=GRID, alpha_fc=0.45, tc=SEC, fs=12.5)
            else:
                ch_cell(ax, i, "q", st["q"], tc=INK, bold=True, fs=12.5,
                        ec=NAVY, lw=1.4)
        else:
            ch_cell(ax, i, "q", st["q"], tc=SEC, fs=12.5)
        if st.get("link", 0) > 0:
            x0 = COL_X0 + i * COL_W + COL_W / 2
            arrow(ax, x0, ROW_H["y"][0] - 2, x0, ROW_H["q"][0] + ROW_H["q"][1] + 2,
                  SEC, lw=1.1, ls=(0, (3, 2)), ms=8, alpha=st["link"], zorder=6)
    if hi_col is not None:
        x0 = COL_X0 + hi_col * COL_W
        rrect(ax, x0 - 1, ROW_H["q"][0] - 4, COL_W + 2,
              ROW_H["y"][0] + ROW_H["y"][1] - ROW_H["q"][0] + 8,
              r=7, ec=NAVY, lw=1.8, zorder=7)
    a1, a2 = rules
    if a1 > 0:
        ax.text(COL_X0, 136, r"$y_t \in \{0,\,1\}$" + "   (¿se produce en el periodo t?)",
                fontsize=11, color=SEC, ha="left", alpha=a1)
    if a2 > 0:
        ax.text(COL_X0, 106,
                r"$Q^{\mathrm{min}} \leq q_t \leq Q^{\mathrm{max}}$ si $y_t = 1$"
                + "   (cantidad solo si está activo)",
                fontsize=11, color=SEC, ha="left", alpha=a2)
    if closing > 0:
        rrect(ax, COL_X0 - 8, ROW_H["q"][0] - 8, 6 * COL_W + 16,
              ROW_H["hdr"][0] + ROW_H["hdr"][1] - ROW_H["q"][0] + 16,
              r=9, ec=C_OK, lw=2.2, alpha=closing, zorder=8)
        ax.text(388, 62, "cromosoma factible", fontsize=13.5, color=INK,
                ha="right", va="center", fontweight="bold", alpha=closing)
        ax.text(400, 61, "✓", fontsize=16, color=C_OK, ha="left",
                va="center", fontweight="bold", alpha=closing)
    return fig


def build_chromosome():
    wtr = GifWriter()
    state = [dict(y=None, q=None, y_set=False, q_set=False) for _ in range(6)]
    rng = np.random.default_rng(11)  # solo para el parpadeo del bit
    fig = ch_frame("cada gen decide apertura y cantidad por periodo",
                   "periodo 0/6", state)
    wtr.add(fig, HOLD_MS)
    r1 = r2 = 0.0
    for i in range(6):
        cnt = f"periodo {i + 1}/6"
        # parpadeo del bit y
        flicker = [str(rng.integers(0, 2)) for _ in range(4)]
        for k, v in enumerate(flicker):
            state[i]["y"] = v
            if i == 0:
                r1 = ease((k + 1) / 4)
            fig = ch_frame("se decide la apertura del periodo:  y_t", cnt,
                           state, hi_col=i, rules=(r1, r2))
            wtr.add(fig)
        state[i]["y"] = str(CH_Y[i])
        state[i]["y_set"] = True
        fig = ch_frame("se decide la apertura del periodo:  y_t", cnt, state,
                       hi_col=i, rules=(r1, r2))
        wtr.add(fig, 250)
        # cantidad q ligada a y
        if CH_Y[i] == 1:
            for k in range(7):
                t = ease((k + 1) / 7)
                if i == 0 or (r2 < 1 and k < 3):
                    r2 = max(r2, ease((k + 1) / 3))
                state[i]["q"] = str(int(round(lerp(QMIN, CH_Q[i], t))))
                state[i]["link"] = 0.7 if k < 3 else 0.0
                fig = ch_frame("la cantidad se acota:  q_t entre Qmin y Qmax",
                               cnt, state, hi_col=i, rules=(r1, r2))
                wtr.add(fig)
            state[i]["q_set"] = True
            state[i]["link"] = 0.0
            fig = ch_frame("la cantidad se acota:  q_t entre Qmin y Qmax",
                           cnt, state, hi_col=i, rules=(r1, r2))
            wtr.add(fig, 250)
        else:
            for k in range(3):
                state[i]["q"] = "0"
                state[i]["link"] = 0.7
                fig = ch_frame("periodo cerrado:  y_t = 0  fuerza  q_t = 0",
                               cnt, state, hi_col=i, rules=(r1, r2))
                wtr.add(fig)
            state[i]["q_set"] = True
            state[i]["link"] = 0.0
            fig = ch_frame("periodo cerrado:  y_t = 0  fuerza  q_t = 0",
                           cnt, state, hi_col=i, rules=(r1, r2))
            wtr.add(fig, 250)
    for k in range(6):
        t = ease((k + 1) / 6)
        fig = ch_frame("todas las restricciones de caja se cumplen",
                       "periodo 6/6", state, rules=(1, 1), closing=t)
        wtr.add(fig)
    wtr.hold(HOLD_MS + 200)
    return wtr


# ============================================================ operadores vecindad
NB_TITLE = "Operadores de vecindad"
NB_Y = [1, 0, 1, 1, 0, 1]
NB_Q = [180, 0, 240, 150, 0, 210]
NB_W, NB_GAP, NB_X0 = 96, 12, 82
NB_YCELL = (278, 52)
NB_QCELL = (222, 52)
NB_OPS = [("N_toggle", C_GA, "salto estructural"),
          ("N_quantity", C_SA, "ajuste fino"),
          ("N_mixta", C_HY, "combinación probabilística")]


def nb_frame(subtitle, cnt, yv, qv, alpha=1.0, hi=None, notes=None,
             legend=0.0):
    """hi: dict col->(color, strength). notes: callables extra."""
    fig = new_fig()
    header(fig, NB_TITLE, subtitle, cnt)
    ax = pixel_axes(fig)
    hi = hi or {}
    for i in range(6):
        x0 = NB_X0 + i * (NB_W + NB_GAP)
        col, stg = hi.get(i, (None, 0.0))
        ec = col if col else GRID
        lw = 1.2 + 1.4 * stg
        rrect(ax, x0, NB_QCELL[0], NB_W, NB_YCELL[0] + NB_YCELL[1] - NB_QCELL[0],
              r=8, ec=ec, lw=lw, alpha=alpha, zorder=3)
        ax.plot([x0 + 6, x0 + NB_W - 6], [NB_YCELL[0], NB_YCELL[0]],
                color=GRID, lw=1.0, alpha=alpha, zorder=3)
        bit_c = NAVY if yv[i] == "1" else SEC
        ax.text(x0 + NB_W / 2, NB_YCELL[0] + 26, yv[i], fontsize=15,
                color=bit_c, ha="center", va="center", fontweight="bold",
                alpha=alpha, zorder=5)
        q_c = INK if qv[i] not in ("0",) else SEC
        ax.text(x0 + NB_W / 2, NB_QCELL[0] + 26, qv[i], fontsize=12,
                color=q_c, ha="center", va="center", alpha=alpha, zorder=5)
        ax.text(x0 + NB_W / 2, NB_QCELL[0] - 18, f"t={i + 1}", fontsize=9,
                color=SEC, ha="center", alpha=alpha, zorder=5)
        ax.text(x0 + 10, NB_YCELL[0] + 41, "y", fontsize=8, color=SEC,
                ha="center", alpha=alpha, zorder=5)
        ax.text(x0 + 10, NB_QCELL[0] + 41, "q", fontsize=8, color=SEC,
                ha="center", alpha=alpha, zorder=5)
    if notes:
        for nt in notes:
            nt(ax)
    if legend > 0:
        cx = [175, 390, 612]
        for (name, col, tag), x in zip(NB_OPS, cx):
            ax.add_patch(Rectangle((x - 62, 108), 14, 14, facecolor=col,
                                   edgecolor="none", alpha=legend, zorder=5))
        for (name, col, tag), x in zip(NB_OPS, cx):
            ax.text(x - 42, 115, name, fontsize=10.5, color=INK, ha="left",
                    va="center", fontweight="bold", alpha=legend, zorder=5)
            ax.text(x - 42, 92, tag, fontsize=9, color=SEC, ha="left",
                    va="center", alpha=legend, zorder=5)
    return fig


def _nb_halo(ax, i, cell, color, t):
    x0 = NB_X0 + i * (NB_W + NB_GAP)
    y0, h = cell
    rrect(ax, x0 - 4 - 6 * t, y0 - 4 - 6 * t, NB_W + 8 + 12 * t,
          h + 8 + 12 * t, r=10, ec=color, lw=2.0, alpha=0.65 * (1 - 0.5 * t),
          zorder=7)


def build_neighborhood():
    wtr = GifWriter()
    base_y = [str(v) for v in NB_Y]
    base_q = [str(v) for v in NB_Q]
    # intro: solución base asentada, sostenida ~1 s
    fig = nb_frame("solución actual (y, q) — su vecindario en SA", "",
                   base_y, base_q)
    wtr.add(fig, HOLD_MS)
    for k in range(2):
        fig = nb_frame("tres operadores generan soluciones vecinas", "",
                       base_y, base_q)
        wtr.add(fig)

    # ---- N_toggle: invierte y_2 (0 -> 1), q_2 se activa
    sub = "N_toggle — invierte un bit:  salto estructural"
    cnt = "operador 1/3"
    for k in range(4):
        t = ease((k + 1) / 4)
        fig = nb_frame(sub, cnt, base_y, base_q,
                       hi={1: (C_GA, t)})
        wtr.add(fig)
    for k in range(6):  # destello + flip
        t = k / 5.0
        yv = base_y.copy()
        yv[1] = "1" if k >= 3 else "0"
        fig = nb_frame(sub, cnt, yv, base_q, hi={1: (C_GA, 1.0)},
                       notes=[lambda ax, t=t: _nb_halo(ax, 1, NB_YCELL, C_GA, t)])
        wtr.add(fig)
    yv = base_y.copy()
    yv[1] = "1"
    for k in range(6):  # q se activa con conteo
        t = ease((k + 1) / 6)
        qv = base_q.copy()
        qv[1] = str(int(round(lerp(QMIN, 190, t))))
        fig = nb_frame(sub, cnt, yv, qv, hi={1: (C_GA, 1.0)},
                       notes=[lambda ax: ax.text(
                           NB_X0 + 1 * (NB_W + NB_GAP) + NB_W / 2, 352,
                           "se activa el periodo", fontsize=9, color=INK,
                           ha="center", zorder=8)])
        wtr.add(fig)
    qv = base_q.copy()
    qv[1] = "190"
    fig = nb_frame(sub, cnt, yv, qv, hi={1: (C_GA, 1.0)})
    wtr.add(fig, 500)
    for k in range(3):  # revertir
        fig = nb_frame("volvemos a la solución actual", cnt, base_y, base_q)
        wtr.add(fig)

    # ---- N_quantity: desliza q_3 (240 -> 205)
    sub = "N_quantity — desliza una cantidad:  ajuste fino"
    cnt = "operador 2/3"
    x3 = NB_X0 + 2 * (NB_W + NB_GAP) + NB_W / 2
    for k in range(4):
        t = ease((k + 1) / 4)
        fig = nb_frame(sub, cnt, base_y, base_q, hi={2: (C_SA, t)})
        wtr.add(fig)
    for k in range(9):
        t = ease((k + 1) / 9)
        qv = base_q.copy()
        qv[2] = str(int(round(lerp(240, 205, t))))

        def note(ax, t=t):
            arrow(ax, x3 + 26, 366, x3 + 26, 344, C_SA, lw=2.0, ms=12,
                  zorder=8)
            ax.text(x3 + 38, 356, "−δ", fontsize=10.5, color=INK, ha="left",
                    va="center", zorder=8)
        fig = nb_frame(sub, cnt, base_y, qv, hi={2: (C_SA, 1.0)}, notes=[note])
        wtr.add(fig)
    qv = base_q.copy()
    qv[2] = "205"
    fig = nb_frame(sub, cnt, base_y, qv, hi={2: (C_SA, 1.0)})
    wtr.add(fig, 500)
    for k in range(3):
        fig = nb_frame("volvemos a la solución actual", cnt, base_y, base_q)
        wtr.add(fig)

    # ---- N_mixta: toggle y_5 + desliza q_1, a la vez
    sub = "N_mixta — ambos a la vez:  combinación probabilística"
    cnt = "operador 3/3"
    x1 = NB_X0 + 0 * (NB_W + NB_GAP) + NB_W / 2
    for k in range(4):
        t = ease((k + 1) / 4)
        fig = nb_frame(sub, cnt, base_y, base_q,
                       hi={4: (C_HY, t), 0: (C_HY, t)})
        wtr.add(fig)
    for k in range(9):
        t = ease((k + 1) / 9)
        yv = base_y.copy()
        yv[4] = "1" if k >= 3 else "0"
        qv = base_q.copy()
        qv[0] = str(int(round(lerp(180, 150, t))))
        qv[4] = str(int(round(lerp(QMIN, 160, t)))) if k >= 3 else "0"
        notes = []
        if k < 6:
            notes.append(lambda ax, t=min(1.0, k / 5.0):
                         _nb_halo(ax, 4, NB_YCELL, C_HY, t))
        notes.append(lambda ax: arrow(ax, x1 + 26, 366, x1 + 26, 344, C_HY,
                                      lw=2.0, ms=12, zorder=8))
        notes.append(lambda ax: ax.text(x1 + 38, 356, "−δ", fontsize=10.5,
                                        color=INK, ha="left", va="center",
                                        zorder=8))
        fig = nb_frame(sub, cnt, yv, qv, hi={4: (C_HY, 1.0), 0: (C_HY, 1.0)},
                       notes=notes)
        wtr.add(fig)
    fig = nb_frame(sub, cnt, yv, qv, hi={4: (C_HY, 1.0), 0: (C_HY, 1.0)})
    wtr.add(fig, 500)

    # cierre con leyenda
    for k in range(6):
        t = ease((k + 1) / 6)
        fig = nb_frame("tres movimientos, tres escalas de cambio", "",
                       base_y, base_q, legend=t)
        wtr.add(fig)
    wtr.hold(HOLD_MS + 200)
    return wtr


# ============================================== exploracion vs explotacion
SP_TITLE = "El espectro exploración–explotación"
SP_BAR = (100, 700, 208, 238)  # x0 x1 y0 y1
CMAP_SPEC = LinearSegmentedColormap.from_list("spec", [BG, NAVY])
SP_LANES = {"GA": 300, "SA": 352, "DE": 150, "GA-SA": 98}
SP_COLORS = {"GA": C_GA, "SA": C_SA, "DE": C_DE, "GA-SA": C_HY}


def sp_chip(ax, name, x, y, alpha=1.0):
    col = SP_COLORS[name]
    w, h = 96, 34
    # conector hacia la barra
    if y > SP_BAR[3]:
        ax.plot([x, x], [SP_BAR[3], y - h / 2], color=GRID, lw=1.2,
                alpha=0.8 * alpha, zorder=2)
    else:
        ax.plot([x, x], [y + h / 2, SP_BAR[2]], color=GRID, lw=1.2,
                alpha=0.8 * alpha, zorder=2)
    rrect(ax, x - w / 2, y - h / 2, w, h, r=12, fc=col, ec=col, lw=1.6,
          alpha=0.9 * alpha, zorder=4)
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=12",
                                facecolor=BG, edgecolor="none",
                                alpha=0.78 * alpha, zorder=5))
    rrect(ax, x - w / 2, y - h / 2, w, h, r=12, fc="none", ec=col, lw=1.8,
          alpha=alpha, zorder=6)
    ax.text(x, y - 1, name, fontsize=10.5, color=INK, ha="center",
            va="center", fontweight="bold", alpha=alpha, zorder=7)


def sp_frame(subtitle, chips, bar_t=1.0, labels_a=1.0):
    fig = new_fig()
    header(fig, SP_TITLE, subtitle, "")
    ax = pixel_axes(fig)
    x0, x1, y0, y1 = SP_BAR
    xe = lerp(x0 + 10, x1, bar_t)
    grad = np.linspace(0, bar_t, 512).reshape(1, -1)
    ax.imshow(grad, extent=(x0, xe, y0, y1), origin="lower", aspect="auto",
              cmap=CMAP_SPEC, vmin=0, vmax=1, zorder=1)
    rrect(ax, x0, y0, x1 - x0, y1 - y0, r=8, ec=GRID, lw=1.4, zorder=3)
    if labels_a > 0:
        ax.text(x0, y0 - 24, "EXPLORACIÓN", fontsize=11, color=INK,
                ha="left", va="center", fontweight="bold", alpha=labels_a)
        ax.text(x1, y0 - 24, "EXPLOTACIÓN", fontsize=11, color=INK,
                ha="right", va="center", fontweight="bold", alpha=labels_a)
        ax.text(x0, y1 + 16, "buscar amplio", fontsize=9, color=SEC,
                ha="left", va="center", alpha=labels_a)
        ax.text(x1, y1 + 16, "refinar lo bueno", fontsize=9, color=SEC,
                ha="right", va="center", alpha=labels_a)
    for name, x, y, a in chips:
        sp_chip(ax, name, x, y, a)
    return fig


def build_spectrum():
    wtr = GifWriter()
    Lga, Lsa, Lde, Lhy = (SP_LANES[k] for k in ("GA", "SA", "DE", "GA-SA"))

    def ga_x(k):     # pulso amplio alrededor de la izquierda
        return 180 + 55 * math.sin(2 * math.pi * k / 14.0)

    def de_x(k):     # pulso moderado centro-izquierda
        return 330 + 18 * math.sin(2 * math.pi * k / 11.0 + 1.2)

    def hy_x(k):     # oscila entre ambas zonas
        return 400 + 180 * math.sin(2 * math.pi * k / 22.0)

    k = 0
    # frame inicial asentado (solo titulo), sostenido ~1 s
    fig = sp_frame("¿dónde busca cada metaheurística?", [], bar_t=0.0,
                   labels_a=0.0)
    wtr.add(fig, HOLD_MS)
    # intro: la barra se dibuja
    for j in range(6):
        t = ease((j + 1) / 6)
        fig = sp_frame("un espectro continuo entre buscar y refinar", [],
                       bar_t=t, labels_a=t)
        wtr.add(fig)
    wtr.hold(400)
    # GA llega (cae desde arriba) y pulsa amplio
    for j in range(5):
        t = ease((j + 1) / 5)
        fig = sp_frame("GA: población diversa — explora en amplio",
                       [("GA", 180, lerp(430, Lga, t), t)])
        wtr.add(fig)
    for j in range(10):
        k += 1
        fig = sp_frame("GA: población diversa — explora en amplio",
                       [("GA", ga_x(k), Lga, 1)])
        wtr.add(fig)
    # DE llega
    for j in range(4):
        t = ease((j + 1) / 4)
        k += 1
        fig = sp_frame("DE: diferencias entre vectores — balance intermedio",
                       [("GA", ga_x(k), Lga, 1),
                        ("DE", 330, lerp(20, Lde, t), t)])
        wtr.add(fig)
    for j in range(6):
        k += 1
        fig = sp_frame("DE: diferencias entre vectores — balance intermedio",
                       [("GA", ga_x(k), Lga, 1), ("DE", de_x(k), Lde, 1)])
        wtr.add(fig)
    # SA se desliza de izquierda a derecha (enfriamiento)
    for j in range(2):
        t = ease((j + 1) / 2)
        k += 1
        fig = sp_frame("SA: parte explorando con T alta…",
                       [("GA", ga_x(k), Lga, 1), ("DE", de_x(k), Lde, 1),
                        ("SA", 150, Lsa, t)])
        wtr.add(fig)
    for j in range(12):
        t = ease((j + 1) / 12)
        k += 1
        sub = ("SA: parte explorando con T alta…" if t < 0.5
               else "…y termina explotando con T baja")
        fig = sp_frame(sub, [("GA", ga_x(k), Lga, 1), ("DE", de_x(k), Lde, 1),
                             ("SA", lerp(150, 630, t), Lsa, 1)])
        wtr.add(fig)
    wtr.hold(300)
    # GA-SA oscila entre ambas zonas
    for j in range(2):
        t = ease((j + 1) / 2)
        k += 1
        fig = sp_frame("GA-SA: alterna fase global y refinamiento local",
                       [("GA", ga_x(k), Lga, 1), ("DE", de_x(k), Lde, 1),
                        ("SA", 630, Lsa, 1), ("GA-SA", hy_x(0), Lhy, t)])
        wtr.add(fig)
    for j in range(18):
        k += 1
        fig = sp_frame("GA-SA: alterna fase global y refinamiento local",
                       [("GA", ga_x(k), Lga, 1), ("DE", de_x(k), Lde, 1),
                        ("SA", 630, Lsa, 1), ("GA-SA", hy_x(j + 1), Lhy, 1)])
        wtr.add(fig)
    # final: todos en su posición característica
    for j in range(12):
        k += 1
        fig = sp_frame("cuatro estrategias, un mismo compromiso",
                       [("GA", ga_x(k), Lga, 1), ("DE", de_x(k), Lde, 1),
                        ("SA", 630, Lsa, 1), ("GA-SA", hy_x(j + 19), Lhy, 1)])
        wtr.add(fig)
    wtr.hold(HOLD_MS + 200)
    return wtr


# ====================================================================== main
BUILDERS = {
    "intuicion_ga.gif": build_ga,
    "intuicion_sa.gif": build_sa,
    "intuicion_de.gif": build_de,
    "intuicion_ga_sa.gif": build_gasa,
    "chromosome_build.gif": build_chromosome,
    "neighborhood_operators.gif": build_neighborhood,
    "exploration_exploitation.gif": build_spectrum,
}
ALIASES = {"ga": "intuicion_ga.gif", "sa": "intuicion_sa.gif",
           "de": "intuicion_de.gif", "gasa": "intuicion_ga_sa.gif",
           "chromosome": "chromosome_build.gif",
           "neighborhood": "neighborhood_operators.gif",
           "spectrum": "exploration_exploitation.gif"}


def contact_sheet(name, wtr, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    n = len(wtr.frames)
    picks = [0, n // 2, n - 1]
    scale = 0.55
    tw, th = int(800 * scale), int(450 * scale)
    pad, cap = 10, 18
    sheet = Image.new("RGB", (3 * tw + 4 * pad, th + 2 * pad + cap), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    for j, p in enumerate(picks):
        im = wtr.frames[p].resize((tw, th))
        x = pad + j * (tw + pad)
        sheet.paste(im, (x, pad))
        d.text((x, pad + th + 4), f"{name}  frame {p + 1}/{n}", fill="#333333")
    out = outdir / f"{Path(name).stem}_contact.png"
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", default="",
                    help="lista separada por comas (ga,sa,de,gasa,chromosome,"
                         "neighborhood,spectrum) o nombres de archivo")
    ap.add_argument("--contact-sheets", default="",
                    help="directorio para hojas de contacto (verificación)")
    ap.add_argument("--max-colors", type=int, default=128)
    args = ap.parse_args()

    names = list(BUILDERS)
    if args.only:
        names = [ALIASES.get(s.strip(), s.strip()) for s in args.only.split(",")]

    OUTDIR.mkdir(parents=True, exist_ok=True)
    report = []
    for name in names:
        wtr = BUILDERS[name]()
        size = write_gif(OUTDIR / name, wtr, colors=args.max_colors)
        report.append((name, len(wtr.frames), size))
        if args.contact_sheets:
            contact_sheet(name, wtr, Path(args.contact_sheets))
        print(f"{name}: {len(wtr.frames)} frames, {size:,} bytes"
              f"{'  [!] > 400 KB' if size > MAX_BYTES else ''}")
    total = sum(r[2] for r in report)
    print(f"total: {total:,} bytes en {len(report)} GIFs")


if __name__ == "__main__":
    main()
