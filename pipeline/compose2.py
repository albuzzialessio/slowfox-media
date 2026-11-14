# -*- coding: utf-8 -*-
import os, sys, subprocess, random, re
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as C
import scenes, scenes_plan
from scenes import Panel

HERE = C.HERE; OUT = C.OUT; CACHE = C.CACHE; BG = C.BG

def render_panel(v, times, total, path):
    sc = scenes_plan.SCENES[v["id"]]
    assert len(sc) == len(v["sentences"]), (len(sc), len(v["sentences"]))
    starts = [0.0] + [max(0.0, times[i][0] - 0.05) for i in range(1, len(times))]
    pn = Panel(v["theme"], v["tag"], sc, starts, total); n = int(total * 30)
    tmp = path + ".part.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "1080x1920", "-r", "30", "-i", "-",
           "-c:v", "libx264", "-crf", "15", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(n): p.stdin.write(np.ascontiguousarray(pn.frame(f / 30.0)).tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, path)

def build(vid, voice="im_nicola", speed=1.17, suffix=""):
    v = next(x for x in C.VIDEOS2 if x["id"] == vid); th = v["theme"]
    audio, times, total = C.tts_all(v, voice, speed)
    raw = os.path.join(CACHE, f"voice_raw_{vid}{suffix}.wav"); sf.write(raw, audio, C.SR)
    voc = os.path.join(CACHE, f"voice_{vid}{suffix}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "highpass=f=75,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=3,loudnorm=I=-15:TP=-1.5:LRA=7", "-ar", "44100", voc], check=True)
    mus = os.path.join(CACHE, f"music_{th}_{int(total)}.wav")
    if not os.path.exists(mus): C.make_music(total, th, mus)
    panel = os.path.join(CACHE, f"panel_{vid}{suffix}.mp4"); render_panel(v, times, total, panel)
    ass = os.path.join(CACHE, f"cap2_{vid}{suffix}.ass"); C.build_ass(v, times, total, ass)
    s = open(ass, encoding="utf-8").read()
    s = s.replace("Style: Cap,Poppins,156,", "Style: Cap,Poppins,128,").replace("pos(540,1340", "pos(540,1335")
    s = "\n".join(l for l in s.split("\n") if ",Tag,,0,0,0," not in l)
    open(ass, "w", encoding="utf-8").write(s)
    final = os.path.join(OUT, f"video_{vid:02d}{suffix}.mp4"); tmp = final + ".part.mp4"
    fc = ("[2:v]subtitles=%s:fontsdir=/usr/share/fonts/truetype/google-fonts,format=yuv420p[v];"
          "[0:a]asplit[vc][vs];[1:a]volume=0.55[mu];[mu][vs]sidechaincompress=threshold=0.03:ratio=9:attack=10:release=350[md];"
          "[vc][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]") % ass
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voc, "-i", mus, "-i", panel,
        "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "19", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, final); print("ok", final, round(total, 1), "s"); return final

if __name__ == "__main__":
    args = sys.argv[1:]; voice = "im_nicola"; suffix = ""
    if "--sara" in args: voice = "if_sara"; suffix = "_sara"; args.remove("--sara")
    for a in args: build(int(a), voice=voice, suffix=suffix)
