# -*- coding: utf-8 -*-
"""Uso: python3 make_episode.py episodes/04.json voce.mp3
Legge l'episodio (JSON), allinea la voce, renderizza il video e crea la copia leggera per l'upload (<3.7 MB)."""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan2, scenes_plan, compose3
import compose as _C
os.makedirs(_C.OUT, exist_ok=True); os.makedirs(_C.CACHE, exist_ok=True)

def load(path):
    ep = json.load(open(path, encoding="utf-8"))
    sents = [tuple(s) if isinstance(s, list) else s for s in ep["sentences"]]
    v = dict(id=ep["id"], tag=ep["tag"], theme=ep["theme"], sentences=sents, caption=ep.get("caption", ""))
    plan2.VIDEOS2[:] = [x for x in plan2.VIDEOS2 if x["id"] != v["id"]] + [v]
    scenes_plan.SCENES[v["id"]] = [(k, p) for k, p in ep["scenes"]]
    return ep, v

def main(path, audio):
    ep, v = load(path)
    assert len(v["sentences"]) == len(ep["scenes"]), "una scena per ogni frase"
    final = compose3.build(v["id"], audio, "_ep")
    small = final.replace(".mp4", "_upload.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", final, "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-maxrate", "380k", "-bufsize", "800k",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", small], check=True)
    print("size", os.path.getsize(final), os.path.getsize(small)); print(final); print(small)
    open(final.replace(".mp4", "_caption.txt"), "w", encoding="utf-8").write(ep["post"])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
