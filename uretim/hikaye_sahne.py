"""Türkçe hikâye metnini sahnelere böler (kural tabanlı; yapay zekâ modeli YOK).
Kullanım: python hikaye_sahne.py hikaye.txt sahneler.json
Her satır bir sahnedir. Tek paragraf verilirse cümleler ikişerli gruplanır.
Tanınan kelimeler (kısıtlı sözlük, serbest metinde sınırlı çalışır):
  yer: yatak, sepet/sandık, kanepe/koltuk  | duygu: şaşkın, üzgün, mutlu | hareket: selam, düşün, sarıl, dans
"""
import json, re, sys

YER = {r"yata[ğk]": ("yatak", -2.9, 0.0, -1.3), r"sepet|sandık": ("sepet", -0.4, 0.35, 3.0), r"kanepe|koltuk": ("kanepe", 3.0, 0.0, 1.45)}
SAYI = {"bir": "1", "iki": "2", "üç": "3"}

def sahne_bol(metin):
    satirlar = [s.strip() for s in metin.strip().splitlines() if s.strip()]
    if len(satirlar) == 1:
        cumle = re.findall(r"[^.!?…]+[.!?…]*", satirlar[0])
        cumle = [c.strip() for c in cumle if c.strip()]
        satirlar = [" ".join(cumle[i:i + 2]) for i in range(0, len(cumle), 2)]
    return satirlar

def analiz(metin):
    t = metin.lower()
    s = {"metin": metin, "yer": None, "egil": False, "duygu": "dogal", "hareket": "bos", "kamera": "genis"}
    for k, (ad, x, y, yaw) in YER.items():
        if re.search(k, t):
            s["yer"] = {"ad": ad, "x": x, "y": y, "yaw": yaw}
            break
    if re.search(r"bakt|baktım|aradı|aradım|altına|içine", t) and s["yer"]:
        s["egil"] = True
    if re.search(r"aaa|şaşır|nerede|ne oldu", t): s["duygu"] = "saskin"
    if re.search(r"yok|kayboldu|üzül|ağla|kayıp", t): s["duygu"] = "uzgun"
    if re.search(r"buldum|mutlu|harika|güzel|sevin|gül|dans|hoş geldin|çok özledim", t): s["duygu"] = "mutlu"
    if re.search(r"merhaba|selam|ben ", t): s["hareket"] = "selam"
    if re.search(r"düşün|hmm", t): s["hareket"] = "dusun"
    if re.search(r"sayal|say:|bir\.\.\. iki", t): s["hareket"] = "say"
    if re.search(r"sarıl|buldum|hoş geldin", t): s["hareket"] = "sarilma"
    if re.search(r"dans", t): s["hareket"] = "dans"
    return s

def sahneler(metin):
    out = [analiz(x) for x in sahne_bol(metin)]
    for i, s in enumerate(out):
        s["kamera"] = "yakin" if i == 0 else ("orta" if s["hareket"] in ("sarilma", "dans") else "genis")
    return out

if __name__ == "__main__":
    sc = sahneler(open(sys.argv[1], encoding="utf-8").read())
    json.dump(sc, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(sc), "sahne")
