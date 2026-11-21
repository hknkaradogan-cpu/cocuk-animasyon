"""sahneler.json + tl.json -> Ara Studio film JSON (ara-studio v2). Kullanım: python film_json.py cikti film.json"""
import json, os, sys
cikti, hedef = sys.argv[1:3]
sc = json.load(open(os.path.join(cikti, "sahneler.json")))
tl = json.load(open(os.path.join(cikti, "tl.json")))
total = tl["total"]
KLIP = {"selam": "wave", "dusun": "look_around", "say": "talk_gestures", "sarilma": "clap", "dans": "dance_groove"}
DUYGU = {"saskin": "look_around", "uzgun": "cry", "mutlu": "cheer"}
beats, shots, texts = [], [], []
n = len(sc)
for i, (s, e) in enumerate(zip(sc, tl["tl"])):
    t0 = 0.0 if i == 0 else e["t0"]
    t1 = total if i == n - 1 else tl["tl"][i + 1]["t0"]
    d = round(max(0.5, min(12, t1 - t0)), 2)
    klip = KLIP.get(s["hareket"]) or DUYGU.get(s["duygu"]) or "talk"
    beats.append({"id": "b%d" % i, "clip": klip, "duration": d, "move": False})
    shots.append({"id": "s%d" % i, "duration": d, "shot": {"yakin": "close", "orta": "medium"}.get(s["kamera"], "medium"), "target": "pirpir"})
    texts.append({"id": "t%d" % i, "text": s["metin"], "style": "subtitle", "anchor": "screen", "start": round(t0, 2),
                  "duration": d, "x": .5, "y": .86, "size": 34, "color": "#ffffff", "background": "#151820"})
film = {"kind": "ara-studio", "version": 2, "title": "Pirpir ve Ayicik", "template": "bedroom",
        "actors": [{"id": "pirpir", "preset": "The Schoolgirl", "params": {"name": "Pirpir"}, "detail": "medium",
                    "x": 0, "y": 0, "z": 0, "yaw": 0, "beats": beats}],
        "shots": shots, "camera": "locked", "view": {"azimuth": 0, "elevation": 4, "zoom": 1},
        "aspect": "portrait", "caption": False, "texts": [], "audio": {"muted": True}}
json.dump(film, open(hedef, "w"), indent=1)
print("film: %d sahne, %.1f sn" % (n, total))
