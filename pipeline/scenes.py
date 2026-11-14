# -*- coding: utf-8 -*-
"""Scene animate vettoriali (skia) per ogni frase. Pannello 1080x900."""
import math, skia, numpy as np

W, H = 1080, 900
FP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
TF = skia.Typeface.MakeFromFile(FP)
_fonts = {}
def font(sz):
    sz = int(sz)
    if sz not in _fonts:
        f = skia.Font(TF, sz); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kSubpixelAntiAlias); _fonts[sz] = f
    return _fonts[sz]

THEMES = {
 "gold":   dict(a=(255, 206, 64),  bg1=(18, 14, 34), bg2=(58, 38, 12)),
 "blue":   dict(a=(90, 200, 255),  bg1=(8, 14, 40),  bg2=(10, 56, 112)),
 "green":  dict(a=(90, 255, 170),  bg1=(8, 24, 24),  bg2=(10, 82, 62)),
 "red":    dict(a=(255, 120, 130), bg1=(30, 10, 18), bg2=(112, 16, 38)),
 "purple": dict(a=(220, 150, 255), bg1=(18, 10, 40), bg2=(72, 22, 122)),
}
PC = [(80, 170, 255), (255, 105, 170), (90, 235, 150), (255, 205, 70)]
WHITE, DARK, RED, GREEN, GRAY = (255, 255, 255), (20, 20, 30), (255, 90, 100), (90, 235, 150), (150, 155, 175)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, s, d): return clamp((t - s) / d) if d > 0 else (1.0 if t >= s else 0.0)
def eo3(x): return 1 - (1 - x) ** 3
def back(x):
    c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def eio(x): return 3 * x * x - 2 * x ** 3
def col(c, a=255): return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(a))

def P(c, a=255, stroke=None, blur=None):
    p = skia.Paint(AntiAlias=True, Color=col(c, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

def R(x, y, w, h): return skia.Rect.MakeXYWH(x, y, w, h)
def rr(cv, x, y, w, h, r, p): cv.drawRRect(skia.RRect.MakeRectXY(R(x, y, w, h), r, r), p)

def fit(s, maxw, size):
    while size > 20 and font(size).measureText(s) > maxw: size -= 2
    return size

def text(cv, s, x, y, size, c=WHITE, a=255, align="c", outline=None, maxw=None):
    if maxw: size = fit(s, maxw, size)
    f = font(size); w = f.measureText(s)
    if align == "c": x -= w / 2
    elif align == "r": x -= w
    if outline: cv.drawString(s, x, y, f, P(outline[0], a, stroke=outline[1]))
    cv.drawString(s, x, y, f, P(c, a))
    return w

def fmt_int(v): return f"{int(round(v)):,}".replace(",", ".")

def path_poly(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p

# ------------------------------------------------------------------ ICONE (coordinate -50..50)
def icon(cv, name, cx, cy, size, c1=WHITE, c2=(255, 206, 64), a=255):
    cv.save(); cv.translate(cx, cy); s = size / 100.0; cv.scale(s, s)
    f1, f2 = P(c1, a), P(c2, a); dk = P(DARK, a)
    st1 = P(c1, a, stroke=9); st2 = P(c2, a, stroke=9); sdk = P(DARK, a, stroke=8)
    if name == "wallet":
        rr(cv, -44, -26, 88, 62, 12, f1); rr(cv, -44, -36, 70, 24, 8, P(c2, a)); rr(cv, 12, -4, 40, 28, 10, f2); cv.drawCircle(28, 10, 5.5, dk)
    elif name == "coin":
        cv.drawCircle(0, 0, 44, f2); cv.drawCircle(0, 0, 33, P(DARK, 60, stroke=5)); text(cv, "€", 0, 18, 56, DARK, a)
    elif name == "house":
        cv.drawPath(path_poly([(-50, -4), (0, -48), (50, -4)]), f2); rr(cv, -34, -6, 68, 50, 4, f1); rr(cv, -9, 14, 18, 30, 3, dk)
    elif name == "bolt":
        cv.drawPath(path_poly([(8, -48), (-28, 6), (-3, 6), (-12, 48), (30, -8), (3, -8)]), f2)
    elif name == "cart":
        cv.drawPath(path_poly([(-46, -34), (-30, -34), (-22, 14), (30, 14)], False), st1)
        cv.drawPath(path_poly([(-26, -18), (44, -18), (34, 6), (-20, 6)]), f2)
        cv.drawCircle(-10, 34, 8, f1); cv.drawCircle(24, 34, 8, f1)
    elif name == "car":
        cv.drawPath(path_poly([(-30, -4), (-18, -30), (20, -30), (32, -4)]), f1); rr(cv, -48, -6, 96, 34, 12, f2)
        cv.drawCircle(-24, 30, 11, f1); cv.drawCircle(24, 30, 11, f1); cv.drawCircle(-24, 30, 4, dk); cv.drawCircle(24, 30, 4, dk)
    elif name == "piggy":
        cv.drawOval(R(-44, -26, 88, 66), f2); cv.drawPath(path_poly([(-22, -22), (-10, -44), (4, -24)]), f2)
        rr(cv, 34, -4, 20, 22, 8, P(c2, a)); cv.drawCircle(40, 8, 3.5, dk); cv.drawCircle(16, -8, 4.5, dk)
        rr(cv, -30, 32, 14, 16, 4, f2); rr(cv, 14, 32, 14, 16, 4, f2); rr(cv, -14, -34, 28, 6, 3, dk)
    elif name == "shield":
        p = skia.Path(); p.moveTo(0, -48); p.cubicTo(18, -36, 32, -34, 42, -34); p.lineTo(42, 4); p.cubicTo(42, 30, 20, 44, 0, 52)
        p.cubicTo(-20, 44, -42, 30, -42, 4); p.lineTo(-42, -34); p.cubicTo(-32, -34, -18, -36, 0, -48); p.close(); cv.drawPath(p, f2)
        cv.drawPath(path_poly([(-18, 2), (-4, 18), (22, -12)], False), sdk)
    elif name == "chartup":
        rr(cv, -42, 6, 20, 38, 4, f1); rr(cv, -10, -10, 20, 54, 4, f1); rr(cv, 22, -28, 20, 72, 4, f2)
        cv.drawPath(path_poly([(-44, -14), (-14, -34), (6, -24), (36, -48)], False), st2)
    elif name == "briefcase":
        rr(cv, -44, -20, 88, 62, 10, f1); cv.drawPath(path_poly([(-16, -20), (-16, -34), (16, -34), (16, -20)], False), st1)
        rr(cv, -44, 6, 88, 6, 0, f2)
    elif name == "medical":
        rr(cv, -42, -42, 84, 84, 18, f1); rr(cv, -9, -26, 18, 52, 4, P(RED, a)); rr(cv, -26, -9, 52, 18, 4, P(RED, a))
    elif name == "gamepad":
        rr(cv, -46, -22, 92, 50, 24, f1); rr(cv, -32, -6, 22, 7, 3, dk); rr(cv, -25, -13, 7, 22, 3, dk)
        cv.drawCircle(20, -4, 6, f2); cv.drawCircle(34, 6, 6, f2)
    elif name == "bag":
        cv.drawPath(path_poly([(-34, -20), (34, -20), (42, 44), (-42, 44)]), f1)
        p = skia.Path(); p.moveTo(-16, -20); p.cubicTo(-16, -50, 16, -50, 16, -20); cv.drawPath(p, st2)
    elif name == "star":
        pts = []
        for i in range(10):
            r = 48 if i % 2 == 0 else 20; ang = -math.pi / 2 + i * math.pi / 5; pts.append((r * math.cos(ang), r * math.sin(ang)))
        cv.drawPath(path_poly(pts), f2)
    elif name == "check":
        cv.drawPath(path_poly([(-30, 2), (-10, 24), (32, -22)], False), P(c1, a, stroke=16))
    elif name == "cross":
        cv.drawPath(path_poly([(-26, -26), (26, 26)], False), P(c1, a, stroke=15)); cv.drawPath(path_poly([(26, -26), (-26, 26)], False), P(c1, a, stroke=15))
    elif name == "clock":
        cv.drawCircle(0, 0, 44, f1); cv.drawPath(path_poly([(0, -26), (0, 0), (20, 12)], False), sdk)
    elif name == "info":
        cv.drawCircle(0, 0, 44, f1); cv.drawCircle(0, -20, 6, dk); rr(cv, -5, -8, 10, 36, 4, dk)
    elif name == "warn":
        cv.drawPath(path_poly([(0, -46), (48, 38), (-48, 38)]), f2); rr(cv, -5, -18, 10, 34, 4, dk); cv.drawCircle(0, 26, 6, dk)
    elif name == "heart":
        p = skia.Path(); p.moveTo(0, 40); p.cubicTo(-60, -4, -34, -50, 0, -20); p.cubicTo(34, -50, 60, -4, 0, 40); cv.drawPath(p, P(RED if c1 == WHITE else c1, a))
    elif name == "bookmark":
        cv.drawPath(path_poly([(-28, -46), (28, -46), (28, 46), (0, 22), (-28, 46)]), f2)
    elif name == "chat":
        rr(cv, -46, -38, 92, 62, 18, f1); cv.drawPath(path_poly([(-20, 20), (-30, 46), (4, 22)]), f1)
        for k in (-20, 0, 20): cv.drawCircle(k, -8, 5, dk)
    elif name == "user":
        cv.drawCircle(0, -16, 18, f1); cv.drawOval(R(-32, 8, 64, 48), f1)
    elif name == "calendar":
        rr(cv, -42, -38, 84, 80, 10, f1); rr(cv, -42, -38, 84, 22, 10, f2); cv.drawCircle(-20, -40, 5, dk); cv.drawCircle(20, -40, 5, dk)
    elif name == "question":
        text(cv, "?", 0, 30, 100, c1, a)
    cv.restore()

# ------------------------------------------------------------------ SFONDO PANNELLO
HF, Y0 = 1920, 250
def panel_bg(cv, th, T, total, tag):
    c1, c2 = th["bg1"], th["bg2"]
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(W * 0.5, HF)], [col(c1), col(c2)]))
    cv.drawRect(R(0, 0, W, HF), p)
    for i, (fx, fy, ph, rad) in enumerate([(0.11, 0.07, 0.0, 520), (0.08, 0.13, 2.0, 460), (0.06, 0.09, 4.0, 400)]):
        x = W * (0.5 + 0.45 * math.sin(T * fx * 2 * math.pi + ph)); y = HF * (0.5 + 0.42 * math.cos(T * fy * 2 * math.pi + ph))
        g = skia.Paint(AntiAlias=True)
        g.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), rad, [col(th["a"], 62), col(th["a"], 0)]))
        cv.drawCircle(x, y, rad, g)
    off = (T * 18) % 60
    dp = P(WHITE, 16)
    for gx in range(-60, W + 60, 60):
        for gy in range(-60, HF + 60, 60): cv.drawCircle(gx + off * 0.5, gy + off, 2.2, dp)
    w = font(34).measureText(tag) + 70
    rr(cv, W / 2 - w / 2, Y0 + 30, w, 62, 31, P(th["a"])); text(cv, tag, W / 2, Y0 + 74, 34, DARK)
    rr(cv, 60, Y0 + H - 34, W - 120, 10, 5, P(WHITE, 40)); rr(cv, 60, Y0 + H - 34, max(10, (W - 120) * T / total), 10, 5, P(th["a"]))

# ------------------------------------------------------------------ SCENE
def sc_bignum(cv, p, t, dur, th):
    a = th["a"]; vf, vt = p.get("from", 0), p.get("to", 0)
    k = eo3(prog(t, 0.1, 1.0)); v = vf + (vt - vf) * k
    pop = back(prog(t, 0, 0.5))
    if p.get("icon"): icon(cv, p["icon"], 540, 285, 190 * pop, WHITE, a)
    s = (p.get("pre", "") + (p["txt"] if "txt" in p else fmt_int(v)) + p.get("suf", ""))
    cv.save(); cv.translate(540, 600); sc = 0.7 + 0.3 * pop; cv.scale(sc, sc)
    text(cv, s, 0, 0, fit(s, 940, p.get("size", 250)), WHITE, 255, outline=((0, 0, 0), 14))
    cv.restore()
    if p.get("label"): text(cv, p["label"], 540, 735, 54, a, 255 * eo3(prog(t, 0.3, 0.4)), maxw=980)
    if p.get("sub"): text(cv, p["sub"], 540, 805, 40, GRAY if "warn" not in p else RED, 255 * eo3(prog(t, 0.5, 0.4)), maxw=980)

def sc_question(cv, p, t, dur, th):
    a = th["a"]; cx, cy = 540, 330
    for i in range(3):
        ph = ((t * 0.7 + i / 3) % 1.0); r = 150 + ph * 190
        cv.drawCircle(cx, cy, r, P(a, int(120 * (1 - ph)), stroke=8))
    pop = back(prog(t, 0, 0.45)); cv.save(); cv.translate(cx, cy); cv.scale(pop, pop)
    cv.drawCircle(0, 0, 150, P(a)); text(cv, "?", 0, 74, 230, DARK); cv.restore()
    for i, ln in enumerate(p["lines"]):
        al = eo3(prog(t, 0.25 + 0.2 * i, 0.4)); text(cv, ln, 540, 640 + i * 96 + (1 - al) * 30, 78, WHITE if i == 0 else a, 255 * al, maxw=980, outline=((0, 0, 0), 10))

def sc_donut(cv, p, t, dur, th):
    parts = p["parts"]; tot = sum(v for _, v, _ in parts); hl = p.get("hl")
    cx, cy, rad, sw = 540, 385, 188, 112
    s = eo3(prog(t, 0.0, 1.0)) if p.get("anim", True) else 1.0
    ang = -90.0; used = 0.0
    for i, (lab, v, ci) in enumerate(parts):
        sweep = 360.0 * v / tot; shown = max(0.0, min(sweep, 360 * s - used)); used += sweep
        dim = hl is not None and i != hl; wid = sw + (26 * eo3(prog(t, 0.3, 0.4)) if hl == i else 0)
        if shown > 1.5:
            pa = P(PC[ci], 70 if dim else 255, stroke=wid); pa.setStrokeCap(skia.Paint.kButt_Cap)
            cv.drawArc(R(cx - rad, cy - rad, 2 * rad, 2 * rad), ang + 0.8, shown - 1.6, False, pa)
        if shown >= sweep - 0.5 and not dim:
            m = math.radians(ang + sweep / 2); tx, ty = cx + rad * math.cos(m), cy + rad * math.sin(m)
            text(cv, f"{int(round(100 * v / tot))}%", tx, ty + 17, 54, DARK if hl is None or hl == i else WHITE)
        ang += sweep
    text(cv, p.get("center", ""), cx, cy + 4, 62, WHITE, maxw=205); text(cv, p.get("csub", ""), cx, cy + 50, 28, GRAY, maxw=205)
    if p.get("icons"):
        n = len(p["icons"]); gap = 230; x0 = 540 - gap * (n - 1) / 2
        for i, (ic, lab) in enumerate(p["icons"]):
            k = back(prog(t, 0.55 + 0.22 * i, 0.4)); icon(cv, ic, x0 + gap * i, 735, 104 * k, WHITE, PC[parts[hl][2]] if hl is not None else th["a"])
            text(cv, lab, x0 + gap * i, 828, 36, WHITE, 255 * clamp(k), maxw=220)
    else:
        n = len(parts); gap = 330; x0 = 540 - gap * (n - 1) / 2
        for i, (lab, v, ci) in enumerate(parts):
            al = eo3(prog(t, 0.7 + 0.15 * i, 0.4)); cv.drawCircle(x0 + gap * i - 80, 790, 15, P(PC[ci], 255 * al)); text(cv, lab, x0 + gap * i - 55, 803, 38, WHITE, 255 * al, align="l", maxw=210)

def sc_bars(cv, p, t, dur, th):
    items = p["items"]; n = len(items); mx = p.get("max", max(v for _, v, _ in items))
    base, top = 690, 190; bw = min(230, 800 / n - 40); gap = (940 - bw * n) / (n + 1)
    if p.get("title"): text(cv, p["title"], 540, 150, 46, WHITE, 255 * eo3(prog(t, 0, 0.4)), maxw=980)
    cv.drawLine(70, base, 1010, base, P(WHITE, 60, stroke=4))
    for i, (lab, v, ci) in enumerate(items):
        g = eo3(prog(t, 0.15 + 0.25 * i, 0.7)); h = (base - top - 40) * v / mx * g
        x = 70 + gap + i * (bw + gap)
        rr(cv, x, base - max(h, 4), bw, max(h, 4), 22, P(PC[ci]))
        txt = (p.get("pre", "") + fmt_int(v * g) + p.get("suf", ""))
        text(cv, txt, x + bw / 2, base - h - 22, fit(txt, bw + gap - 10, 58), WHITE, 255 * clamp(g * 2), outline=((0, 0, 0), 8))
        text(cv, lab, x + bw / 2, base + 62, 40, WHITE, 255 * clamp(g * 2), maxw=bw + gap - 8)
    if p.get("sub"): text(cv, p["sub"], 540, 820, 38, GRAY, 255 * eo3(prog(t, 0.8, 0.4)), maxw=980)

def sc_pairbars(cv, p, t, dur, th):
    groups = p["groups"]; reveal = p["reveal"]; mx = max(b for _, _, b in groups)
    base, top = 690, 200; bw = 128; gx = [200, 540, 880]
    cv.drawLine(70, base, 1010, base, P(WHITE, 60, stroke=4))
    for i, (lab, a_, b_) in enumerate(groups):
        if i >= reveal: break
        cur = (i == reveal - 1); al = 255 if cur else 110
        g = eo3(prog(t, 0.1, 0.8)) if cur else 1.0
        for j, (v, c) in enumerate([(a_, PC[0]), (b_, th["a"])]):
            h = (base - top - 60) * v / mx * g; x = gx[i] + (j - 1) * (bw + 10) + 5
            rr(cv, x, base - max(h, 4), bw, max(h, 4), 18, P(c, al))
            if cur or True:
                text(cv, f"{int(round(v * g))}k", x + bw / 2, base - h - 18, 44, WHITE, al * clamp(g * 2), outline=((0, 0, 0), 7))
        text(cv, f"{lab} anni", gx[i], base + 62, 46, WHITE, al)
    for j, (lab, c) in enumerate([(p["la"], PC[0]), (p["lb"], th["a"])]):
        x = 300 + j * 340; cv.drawCircle(x, 826, 15, P(c)); text(cv, lab, x + 28, 838, 38, WHITE, align="l")

def sc_growth(cv, p, t, dur, th):
    a = th["a"]; x0, x1, yb, yt = 110, 980, 690, 210; r = 0.07 / 12; N = 360
    def fv(m): return ((1 + r) ** m - 1) / r
    k = eo3(prog(t, 0.1, 2.4)); m_end = N * k
    pts = [(x0 + (x1 - x0) * m / N, yb - (yb - yt) * fv(m) / fv(N)) for m in np.linspace(0, m_end, 80)]
    cv.drawLine(x0, yb, x1 + 10, yb, P(WHITE, 60, stroke=4))
    lin = [(x0 + (x1 - x0) * m / N, yb - (yb - yt) * (m / N) * (72000 / 244000)) for m in np.linspace(0, m_end, 40)]
    if len(lin) > 1: cv.drawPath(path_poly(lin, False), P(PC[0], 255, stroke=9))
    if len(pts) > 1:
        area = path_poly(pts + [(pts[-1][0], yb), (pts[0][0], yb)])
        g = skia.Paint(AntiAlias=True); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, yt), skia.Point(0, yb)], [col(a, 120), col(a, 0)])); cv.drawPath(area, g)
        cv.drawPath(path_poly(pts, False), P(a, 255, stroke=13)); cv.drawCircle(pts[-1][0], pts[-1][1], 17, P(WHITE)); cv.drawCircle(pts[-1][0], pts[-1][1], 28, P(a, 90))
    for lab, xx in (("0", x0), ("10", x0 + (x1 - x0) / 3), ("20", x0 + 2 * (x1 - x0) / 3), ("30 anni", x1 - 30)): text(cv, lab, xx, yb + 54, 34, GRAY)
    for j, (lab, c) in enumerate([(p.get("la", "Versato"), PC[0]), (p.get("lb", "Con interesse composto"), a)]):
        x = 140 + j * 330; cv.drawCircle(x, 810, 14, P(c)); text(cv, lab, x + 26, 822, 34, WHITE, align="l")

def sc_list(cv, p, t, dur, th):
    a = th["a"]; items = p["items"]; n = len(items); gap = min(170, 600 / n)
    y0 = 450 - gap * (n - 1) / 2 + 20
    if p.get("title"): text(cv, p["title"], 540, 175, 50, a, 255 * eo3(prog(t, 0, 0.4)), maxw=980); y0 += 40
    for i, (ic, s) in enumerate(items):
        k = prog(t, 0.2 + 0.5 * i, 0.45); e = back(k); al = 255 * clamp(k * 2); y = y0 + i * gap
        cv.save(); cv.translate((1 - eo3(k)) * 120, 0)
        rr(cv, 70, y - 66, 940, 132, 36, P(WHITE, 26 * clamp(k * 2)))
        cc = RED if ic == "cross" else (GREEN if ic == "check" else a)
        cv.drawCircle(150, y, 46 * e, P(cc, al)); icon(cv, ic, 150, y, 58 * e, DARK if ic in ("cross", "check") else DARK, DARK)
        text(cv, s, 225, y + 18, 56, WHITE, al, align="l", maxw=760)
        cv.restore()

def sc_icons(cv, p, t, dur, th):
    a = th["a"]; items = p["items"]; n = len(items); cw = min(290, 940 / n - 30); gap = (980 - cw * n) / (n + 1)
    if p.get("title"): text(cv, p["title"], 540, 175, 52, WHITE, 255 * eo3(prog(t, 0, 0.4)), maxw=980)
    for i, (ic, lab) in enumerate(items):
        k = back(prog(t, 0.2 + 0.4 * i, 0.5)); x = 50 + gap + i * (cw + gap)
        cv.save(); cv.translate(x + cw / 2, 480); cv.scale(max(k, 0.01), max(k, 0.01))
        rr(cv, -cw / 2, -190, cw, 400, 44, P(WHITE, 30)); rr(cv, -cw / 2, -190, cw, 400, 44, P(a, 150, stroke=4))
        icon(cv, ic, 0, -50, cw * 0.58, WHITE, a); text(cv, lab, 0, 150, 40, WHITE, maxw=cw - 24)
        cv.restore()
    if p.get("sub"): text(cv, p["sub"], 540, 800, 40, GRAY, 255 * eo3(prog(t, 1.0, 0.4)), maxw=980)

def sc_split(cv, p, t, dur, th):
    a = th["a"]; cw, ch = 455, 560; xs = [60, 565]
    for i, side in enumerate((p["l"], p["r"])):
        k = back(prog(t, 0.1 + 0.3 * i, 0.5)); good = side.get("good", i == 1); c = a if good else (200, 205, 225)
        cv.save(); cv.translate(xs[i] + cw / 2, 120 + ch / 2 + 20); cv.scale(max(k, 0.01), max(k, 0.01))
        rr(cv, -cw / 2, -ch / 2, cw, ch, 40, P(WHITE, 28)); rr(cv, -cw / 2, -ch / 2, cw, ch, 40, P(c, 200 if good else 90, stroke=6))
        icon(cv, side["icon"], 0, -ch / 2 + 95, 120, WHITE, c)
        text(cv, side["title"], 0, -ch / 2 + 215, 38, GRAY if not good else WHITE, maxw=cw - 40)
        text(cv, side["value"], 0, 75, fit(side["value"], cw - 40, 120), c, outline=((0, 0, 0), 10))
        text(cv, side["sub"], 0, 150, 38, WHITE, maxw=cw - 40)
        if side.get("line2"): text(cv, side["line2"], 0, 205, 34, GRAY, maxw=cw - 40)
        cv.restore()
    if p.get("foot"): text(cv, p["foot"], 540, 800, 40, a, 255 * eo3(prog(t, 0.9, 0.4)), maxw=980)

def sc_calendar(cv, p, t, dur, th):
    a = th["a"]; marks = p.get("marks", []); bw, bh, gx, gy = 215, 150, 22, 22
    x0 = (W - (bw * 4 + gx * 3)) / 2; y0 = 175
    for m in range(12):
        r, c = divmod(m, 4); x = x0 + c * (bw + gx); y = y0 + r * (bh + gy)
        colr, fillp = (255, 255, 255), 24; k = prog(t, 0.1 + 0.11 * m, 0.3)
        for (upto, cc) in marks:
            if m < upto: colr, fillp = cc, 255
        e = eo3(prog(t, 0.1 + 0.11 * m, 0.3))
        base_p = P(WHITE, 24); rr(cv, x, y, bw, bh, 28, base_p)
        if fillp > 30 and e > 0:
            cv.save(); cv.translate(x + bw / 2, y + bh / 2); sc = 0.6 + 0.4 * back(k); cv.scale(sc, sc); rr(cv, -bw / 2, -bh / 2, bw, bh, 28, P(colr, 255 * e)); cv.restore()
        text(cv, str(m + 1), x + bw / 2, y + bh / 2 + 20, 70, DARK if (fillp > 30 and e > 0.5) else WHITE)
    text(cv, p.get("label", ""), 540, 770, 62, WHITE, 255 * eo3(prog(t, 0.5, 0.5)), maxw=980, outline=((0, 0, 0), 8))
    text(cv, p.get("sub", ""), 540, 835, 38, GRAY, 255 * eo3(prog(t, 0.7, 0.5)), maxw=980)

def sc_hero(cv, p, t, dur, th):
    """Icona grande + etichetta (scudo, salvadanaio, ecc.) con monete che cadono se richiesto."""
    a = th["a"]; pop = back(prog(t, 0, 0.55)); cy = 340 + 8 * math.sin(t * 3)
    cv.drawCircle(540, cy, 230 * pop, P(a, 40)); cv.drawCircle(540, cy, 170 * pop, P(a, 50))
    if p.get("coins"):
        for i in range(5):
            ph = ((t * 1.1 + i * 0.2) % 1.0); y = 150 + ph * 160; icon(cv, "coin", 540 + (i - 2) * 36 + (0 if i % 2 else 10), y, 64, WHITE, (255, 205, 70), 255 * (1 - max(0, ph - 0.8) * 5))
    icon(cv, p["icon"], 540, cy + (60 if p.get("coins") else 0), 330 * pop, WHITE, a)
    for i, ln in enumerate(p["lines"]):
        al = eo3(prog(t, 0.3 + 0.2 * i, 0.4)); text(cv, ln, 540, 640 + i * 92 + (1 - al) * 26, 82 if i == 0 else 48, WHITE if i == 0 else a, 255 * al, maxw=980, outline=((0, 0, 0), 9) if i == 0 else None)

def sc_cta(cv, p, t, dur, th):
    a = th["a"]; items = p.get("items", [("bookmark", "Salva"), ("chat", "Commenta"), ("heart", "Segui")]); gap = 300
    text(cv, p.get("title", "Ti è servito?"), 540, 220, 74, WHITE, 255 * eo3(prog(t, 0, 0.4)), maxw=980, outline=((0, 0, 0), 9))
    for i, (ic, lab) in enumerate(items):
        k = back(prog(t, 0.25 + 0.3 * i, 0.5)); x = 540 + (i - 1) * gap; bounce = 1 + 0.06 * math.sin(t * 6 + i)
        cv.drawCircle(x, 470, 125 * k * bounce, P(a, 255 * clamp(k))); icon(cv, ic, x, 470, 150 * k * bounce, DARK if ic != "heart" else WHITE, DARK if ic != "heart" else WHITE)
        text(cv, lab, x, 670, 52, WHITE, 255 * clamp(k))
    if p.get("sub"): text(cv, p["sub"], 540, 790, 44, a, 255 * eo3(prog(t, 1.0, 0.4)), maxw=980)

def sc_words(cv, p, t, dur, th):
    a = th["a"]
    if p.get("icon"): icon(cv, p["icon"], 540, 250, 220 * back(prog(t, 0, 0.5)), WHITE, a)
    for i, ln in enumerate(p["lines"]):
        al = eo3(prog(t, 0.2 + 0.25 * i, 0.4)); text(cv, ln, 540, 540 + i * 100 + (1 - al) * 30, 76, a if i % 2 else WHITE, 255 * al, maxw=980, outline=((0, 0, 0), 9))

SCENES = dict(bignum=sc_bignum, question=sc_question, donut=sc_donut, bars=sc_bars, pairbars=sc_pairbars, growth=sc_growth,
              list=sc_list, icons=sc_icons, split=sc_split, calendar=sc_calendar, hero=sc_hero, cta=sc_cta, words=sc_words)

class Panel:
    def __init__(self, theme, tag, scenes, starts, total):
        self.th = THEMES[theme]; self.tag = tag; self.scenes = scenes; self.starts = starts; self.total = total
        self.surf = skia.Surface(W, HF); self.cv = self.surf.getCanvas()
    def frame(self, T):
        cv = self.cv; cv.clear(skia.ColorBLACK); panel_bg(cv, self.th, T, self.total, self.tag)
        i = 0
        for k, s in enumerate(self.starts):
            if T >= s: i = k
        t = T - self.starts[i]; dur = (self.starts[i + 1] if i + 1 < len(self.starts) else self.total) - self.starts[i]
        TR = 0.3
        def draw(idx, tt, d, alpha, dx):
            cv.save(); cv.translate(dx, Y0); cv.saveLayerAlpha(R(-200, 0, W + 400, H), int(255 * clamp(alpha)))
            kind, par = self.scenes[idx]; SCENES[kind](cv, par, tt, d, self.th); cv.restore(); cv.restore()
        if i > 0 and t < TR:
            pr = eo3(t / TR); pd = self.starts[i] - self.starts[i - 1]
            draw(i - 1, pd + t, pd, 1 - pr, -90 * pr); draw(i, t, dur, pr, 90 * (1 - pr))
        else: draw(i, t, dur, 1.0, 0)
        return self.surf.makeImageSnapshot().toarray()
