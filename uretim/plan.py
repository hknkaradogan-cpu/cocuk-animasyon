"""Hikâye → sahneler → Piper Türkçe seslendirme → zaman çizelgesi.
Çıktılar (cikti klasörü): sahneler.json, tl.json (sahne süreleri + ağız zarfı), voice.wav, altyazi.json
Kullanım: python plan.py hikaye.txt cikti/ [ses_modeli]"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hikaye_sahne import sahneler

hikaye, cikti = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "tr_TR-dfki-medium"
FPS = 12
os.makedirs(cikti, exist_ok=True)
sc = sahneler(open(hikaye, encoding="utf-8").read())
parcalar, sr = [], None
for i, s in enumerate(sc):
    f = os.path.join(cikti, "s%02d.wav" % i)
    r = subprocess.run([sys.executable, "-m", "piper", "-m", model, "-f", f], input=s["metin"].encode("utf-8"),
                       capture_output=True)
    if r.returncode != 0 or not os.path.exists(f):
        raise SystemExit("Piper hatası (sahne %d): %s" % (i, r.stderr.decode("utf-8", "ignore")[-500:]))
    w = wave.open(f)
    sr = w.getframerate()
    parcalar.append(np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768)
tl2, t = [], 0.4
onceki = None
for i, (s, a) in enumerate(zip(sc, parcalar)):
    yer = s["yer"]["ad"] if s["yer"] else None
    if i > 0:
        t += 1.6 if (yer and yer != onceki) else (1.2 if s["hareket"] in ("sarilma", "dans") else 0.7)
    d = len(a) / sr
    tl2.append({"t0": round(t, 3), "d": round(d, 3), "_a": i})
    t += d
    if yer:
        onceki = yer
total = t + 2.0
out = np.zeros(int(sr * total) + 1, dtype=np.float32)
for e, a in zip(tl2, parcalar):
    out[int(e["t0"] * sr):int(e["t0"] * sr) + len(a)] = a
n = int(total * FPS)
env = []
for f in range(n):
    x = out[int(f / FPS * sr):int((f + 1) / FPS * sr)]
    env.append(float(np.sqrt((x ** 2).mean())) if len(x) else 0.0)
m = max(env) or 1
env = [round(min(1, e / m * 1.5), 3) for e in env]
import scipy.io.wavfile as wf
wf.write(os.path.join(cikti, "voice.wav"), sr, (np.clip(out, -1, 1) * 32767).astype(np.int16))
json.dump({"tl": [{"t0": e["t0"], "d": e["d"]} for e in tl2], "env": env, "total": total, "fps": FPS},
          open(os.path.join(cikti, "tl.json"), "w"))
json.dump(sc, open(os.path.join(cikti, "sahneler.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("sahne:", len(sc), "süre: %.1f sn" % total, "kare:", n, "örnekleme:", sr)
