# -*- coding: utf-8 -*-
import os, sys, re, hashlib, subprocess, random
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan2 import VIDEOS2, plain, spoken

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); CACHE = os.path.join(HERE, "cache"); BG = os.path.join(HERE, "bg")
for d in (OUT, CACHE): os.makedirs(d, exist_ok=True)
SR = 24000
ACC = {"gold": (255, 214, 64), "blue": (90, 200, 255), "green": (90, 255, 170), "red": (255, 120, 130), "purple": (220, 150, 255)}
KEYS = {"gold": 1.0, "blue": 1.122, "green": 0.94, "red": 1.06, "purple": 1.19}   # trasposizione musicale
BPM = {"gold": 96, "blue": 88, "green": 92, "red": 100, "purple": 90}

_k = None
def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(HERE, "models/kokoro-v1.0.onnx"), os.path.join(HERE, "models/voices-v1.0.bin"))
    return _k

def trim(s, thr=0.012):
    idx = np.where(np.abs(s) > thr)[0]
    return s if len(idx) == 0 else s[max(0, idx[0] - 120): idx[-1] + 300]

def tts_all(v, voice, speed):
    parts, times, t = [np.zeros(int(0.1 * SR), np.float32)], [], 0.1
    for i, s in enumerate(v["sentences"]):
        txt = spoken(s); key = hashlib.md5(f"{voice}|{speed}|{txt}".encode()).hexdigest()[:16]
        cf = os.path.join(CACHE, f"s_{key}.npy")
        if os.path.exists(cf): a = np.load(cf)
        else:
            a, sr = kokoro().create(txt, voice=voice, speed=speed, lang="it"); a = trim(a.astype(np.float32)); np.save(cf, a)
        dur = len(a) / SR; gap = 0.28 if i == 0 else 0.14
        times.append((t, t + dur)); parts += [a, np.zeros(int(gap * SR), np.float32)]; t += dur + gap
    parts.append(np.zeros(int(0.5 * SR), np.float32)); t += 0.5
    return np.concatenate(parts), times, t

def make_music(total, theme, path):
    sr = 44100; n = int((total + 1) * sr); out = np.zeros(n, np.float32)
    bpm = BPM[theme]; beat = 60 / bpm; k = KEYS[theme]; rng = np.random.default_rng(5)
    def add(sig, at):
        i = int(at * sr); j = min(n, i + len(sig))
        if i < n: out[i:j] += sig[: j - i]
    tk = np.arange(int(0.28 * sr)) / sr
    kick = np.sin(2 * np.pi * np.cumsum(46 + 80 * np.exp(-tk * 30)) / sr) * np.exp(-tk * 13) * 0.9
    th = np.arange(int(0.18 * sr)) / sr
    clap = np.convolve(rng.standard_normal(len(th)), np.ones(4) / 4, "same") * np.exp(-th * 24) * 0.35
    hat = np.diff(rng.standard_normal(int(0.06 * sr) + 1)) * np.exp(-np.arange(int(0.06 * sr)) / sr * 90) * 0.18
    chords = [(220, 261.63, 329.63), (174.61, 220, 261.63), (261.63, 329.63, 392), (196, 246.94, 293.66)]
    roots = [55, 43.65, 65.41, 49]
    nb = int((total + 1) / beat) + 1
    for b in range(nb):
        at = b * beat; bar = (b // 4) % 4
        if b % 4 in (0, 2): add(kick, at)
        if b % 4 == 3: add(kick, at + beat * 0.5)
        if b % 4 in (1, 3): add(clap, at)
        add(hat, at); add(hat * 0.6, at + beat * 0.5)
        if b % 2 == 0:
            tb = np.arange(int(beat * 1.9 * sr)) / sr
            add(np.sin(2 * np.pi * roots[bar] * k * tb) * np.exp(-tb * 2.2) * 0.55, at)
    tp = np.arange(n) / sr; bar_idx = ((tp / (beat * 4)).astype(int)) % 4; pad = np.zeros(n, np.float32)
    for bi, ch in enumerate(chords):
        m = (bar_idx == bi).astype(np.float32); m = np.convolve(m, np.ones(2000) / 2000, "same")
        pad += m * sum(np.sin(2 * np.pi * f * k * tp) for f in ch) / 3 * 0.10
    out += pad.astype(np.float32)
    out *= 0.7 / max(1e-6, np.abs(out).max()); out[: int(sr * 0.5)] *= np.linspace(0, 1, int(sr * 0.5))
    sf.write(path, out, sr)

def ass_col(c): return "&H%02X%02X%02X&" % (c[2], c[1], c[0])
def fmt(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def chunks_for(shown):
    words = shown.split(); out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 3 or re.search(r"[,.:;?!]$", w) or sum(len(x) for x in cur) > 15:
            out.append(cur); cur = []
    if cur: out.append(cur)
    # evita chunk finale di una sola parola corta
    if len(out) > 1 and len(out[-1]) == 1 and len(out[-1][0]) <= 3 and len(out[-2]) < 3:
        out[-2] += out.pop()
    return out

def build_ass(v, times, total, path):
    acc = ass_col(ACC[v["theme"]])
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,156,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,&H00000000&,-1,0,0,0,100,100,0,0,1,14,3,5,50,50,0,1
Style: Tag,Poppins,56,&H00181818&,&H00181818&,{acc},&H00000000&,-1,0,0,0,100,100,2,0,3,20,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{fmt(0)},{fmt(total)},Tag,,0,0,0,,{{\\an5\\pos(540,300)}}{v['tag']}"]
    for si, s in enumerate(v["sentences"]):
        a, b = times[si]; dur = b - a; ch = chunks_for(plain(s))
        wts = []
        for c in ch:
            for w in c: wts.append(len(w) + 1.5 + (3 if re.search(r"[,.:;?!]$", w) else 0))
        cum = np.concatenate([[0], np.cumsum(wts)]) / sum(wts); wi = 0
        for ci, c in enumerate(ch):
            for k, w in enumerate(c):
                ws = a + cum[wi] * dur - 0.04; we = a + cum[wi + 1] * dur - 0.04
                if k == len(c) - 1: we = min(we + 0.12, (times[si + 1][0] if si + 1 < len(times) else total))
                text = " ".join((f"{{\\c{acc}}}{x.upper()}{{\\c&HFFFFFF&}}" if j == k else x.upper()) for j, x in enumerate(c))
                pop = "\\fscx70\\fscy70\\t(0,90,\\fscx108\\fscy108)\\t(90,170,\\fscx100\\fscy100)" if k == 0 else ""
                ev.append(f"Dialogue: 1,{fmt(ws)},{fmt(we)},Cap,,0,0,0,,{{\\an5\\pos(540,1340){pop}}}{text}")
                wi += 1
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")

def build(vid, voice="im_nicola", speed=1.17, suffix=""):
    v = next(x for x in VIDEOS2 if x["id"] == vid); th = v["theme"]
    audio, times, total = tts_all(v, voice, speed)
    raw = os.path.join(CACHE, f"voice_raw_{vid}{suffix}.wav"); sf.write(raw, audio, SR)
    voc = os.path.join(CACHE, f"voice_{vid}{suffix}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "highpass=f=75,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3,loudnorm=I=-15:TP=-1.5:LRA=7", "-ar", "44100", voc], check=True)
    mus = os.path.join(CACHE, f"music_{th}_{int(total)}.wav")
    if not os.path.exists(mus): make_music(total, th, mus)
    ass = os.path.join(CACHE, f"cap_{vid}{suffix}.ass"); build_ass(v, times, total, ass)
    bgf = os.path.join(BG, f"bg_{th}.mp4")
    dur_bg = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", bgf]).decode().strip())
    off = random.Random(vid * 7).uniform(0, max(0, dur_bg - total - 1))
    final = os.path.join(OUT, f"video_{vid:02d}{suffix}.mp4"); tmp = final + ".part.mp4"
    fc = ("[0:v]eq=brightness=-0.05:saturation=1.15,subtitles=%s:fontsdir=/usr/share/fonts/truetype/google-fonts,format=yuv420p[v];"
          "[1:a]asplit[vc][vs];[2:a]volume=0.55[mu];[mu][vs]sidechaincompress=threshold=0.03:ratio=9:attack=10:release=350[md];"
          "[vc][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]") % ass
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{off:.2f}", "-t", f"{total:.2f}", "-i", bgf, "-i", voc, "-i", mus,
        "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "21", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, final); print("ok", final, round(total, 1), "s")
    return final

if __name__ == "__main__":
    args = sys.argv[1:]; voice = "im_nicola"; suffix = ""
    if "--sara" in args: voice = "if_sara"; suffix = "_sara"; args.remove("--sara")
    for a in args: build(int(a), voice=voice, suffix=suffix)
