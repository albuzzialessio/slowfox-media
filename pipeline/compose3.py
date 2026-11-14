# -*- coding: utf-8 -*-
"""Montaggio con voce esterna (ElevenLabs): allinea frasi e parole alle pause dell'audio."""
import os, sys, re, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as C
import compose2 as C2
from plan2 import VIDEOS2, plain, spoken

HERE = C.HERE; OUT = C.OUT; CACHE = C.CACHE

def sil_detect(path, noise="-38dB", d=0.2):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())
    sils = []
    for i, s in enumerate(st):
        e = en[i] if i < len(en) else dur; sils.append((s, e))
    return sils, dur

def words_of(s): return plain(s).split()
def wts_of(ws): return [len(w) + 1.5 + (3 if re.search(r"[,.:;?!]$", w) else 0) for w in ws]

def align(v, path):
    sils, dur = sil_detect(path)
    s0 = sils[0][1] if sils and sils[0][0] < 0.05 else 0.0
    e0 = sils[-1][0] if sils and sils[-1][1] >= dur - 0.05 else dur
    sils = [x for x in sils if x[0] > s0 + 0.05 and x[1] < e0 - 0.05]
    sents = v["sentences"]; n = len(sents)
    chars = np.array([len(spoken(s)) for s in sents], float); cum = np.cumsum(chars) / chars.sum()
    # un confine per ogni coppia di frasi: scegli la pausa più lunga vicino alla posizione attesa
    used = []; last = -1
    for k in range(n - 1):
        exp = s0 + cum[k] * (e0 - s0); best, bs = None, 1e9
        for j, (a, b) in enumerate(sils):
            if j <= last: continue
            m = (a + b) / 2; cost = abs(m - exp) / 1.2 - (b - a) * 3.0
            if abs(m - exp) < 3.5 and cost < bs: best, bs = j, cost
        if best is None:  # nessuna pausa: usa la posizione attesa
            used.append((exp, exp, None))
        else: used.append((sils[best][0], sils[best][1], best)); last = best
    times = []; inner = []
    for k in range(n):
        a = s0 if k == 0 else used[k - 1][1]; b = e0 if k == n - 1 else used[k][0]
        times.append((a, b))
    taken = {u[2] for u in used if u[2] is not None}
    for k in range(n):
        a, b = times[k]; ws = words_of(sents[k]); wt = wts_of(ws); c = np.concatenate([[0], np.cumsum(wt)]) / sum(wt)
        cand = [(x, y) for j, (x, y) in enumerate(sils) if j not in taken and x > a + 0.1 and y < b - 0.05]; anchors = []; pj = -1
        for wi, w in enumerate(ws[:-1]):
            if not re.search(r"[,:;?!]$", w): continue
            exp = a + c[wi + 1] * (b - a); bi, bd = None, 0.7
            for j, (x, y) in enumerate(cand):
                if j <= pj: continue
                dd = abs((x + y) / 2 - exp)
                if dd < bd: bi, bd = j, dd
            if bi is not None: anchors.append((c[wi + 1], (cand[bi][0] + cand[bi][1]) / 2)); pj = bi
        inner.append(anchors)
    return times, inner, s0, e0, dur

def build_ass3(v, times, inner, total, path):
    C.build_ass(v, times, total, path)  # intestazione e stili
    head = open(path, encoding="utf-8").read().split("[Events]")[0]
    head = head.replace("Style: Cap,Poppins,156,", "Style: Cap,Poppins,128,")
    acc = C.ass_col(C.ACC[v["theme"]]); ev = []
    for si, s in enumerate(v["sentences"]):
        a, b = times[si]; ch = C.chunks_for(plain(s)); ws = [w for c in ch for w in c]
        wt = wts_of(ws); c = np.concatenate([[0], np.cumsum(wt)]) / sum(wt)
        xs = [0.0] + [f for f, _ in inner[si]] + [1.0]; ys = [a] + [t for _, t in inner[si]] + [b]
        T = lambda f: float(np.interp(f, xs, ys)); wi = 0
        nxt = times[si + 1][0] if si + 1 < len(times) else total
        for cc in ch:
            for k, w in enumerate(cc):
                ws_, we_ = T(c[wi]) - 0.04, T(c[wi + 1]) - 0.04
                if k == len(cc) - 1: we_ = min(we_ + 0.12, nxt)
                text = " ".join((f"{{\\c{acc}}}{x.upper()}{{\\c&HFFFFFF&}}" if j == k else x.upper()) for j, x in enumerate(cc))
                pop = "\\fscx70\\fscy70\\t(0,90,\\fscx108\\fscy108)\\t(90,170,\\fscx100\\fscy100)" if k == 0 else ""
                ev.append(f"Dialogue: 1,{C.fmt(ws_)},{C.fmt(we_)},Cap,,0,0,0,,{{\\an5\\pos(540,1335){pop}}}{text}")
                wi += 1
    open(path, "w", encoding="utf-8").write(head + "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(ev) + "\n")

def build(vid, audio, suffix="_leo"):
    v = next(x for x in VIDEOS2 if x["id"] == vid); th = v["theme"]
    times, inner, s0, e0, dur = align(v, audio); total = dur + 0.5
    print("frasi", [(round(a, 1), round(b, 1)) for a, b in times], "interne", [len(x) for x in inner])
    voc = os.path.join(CACHE, f"voice_ext_{vid}{suffix}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", audio, "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90:makeup=2,loudnorm=I=-15:TP=-1.5:LRA=7,apad=pad_dur=1", "-ar", "44100", "-t", f"{total:.2f}", voc], check=True)
    mus = os.path.join(CACHE, f"music_{th}_{int(total)}.wav")
    if not os.path.exists(mus): C.make_music(total, th, mus)
    panel = os.path.join(CACHE, f"panel_{vid}{suffix}.mp4"); C2.render_panel(v, times, total, panel)
    ass = os.path.join(CACHE, f"cap3_{vid}{suffix}.ass"); build_ass3(v, times, inner, total, ass)
    final = os.path.join(OUT, f"video_{vid:02d}{suffix}.mp4"); tmp = final + ".part.mp4"
    fc = ("[2:v]subtitles=%s:fontsdir=/usr/share/fonts/truetype/google-fonts,format=yuv420p[v];"
          "[0:a]asplit[vc][vs];[1:a]volume=0.45[mu];[mu][vs]sidechaincompress=threshold=0.03:ratio=9:attack=10:release=350[md];"
          "[vc][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]") % ass
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voc, "-i", mus, "-i", panel, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}",
        "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, final); print("ok", final, round(total, 1)); return final

if __name__ == "__main__":
    build(int(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "_leo")
