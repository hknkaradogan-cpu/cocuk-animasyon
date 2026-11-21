"""Segmentleri birleştirir, altyazı + seslendirme + müzik ekler, MP4 üretir ve gerçek ölçümleri yazar.
Kullanım: python birlestir.py cikti segs cikti/video.mp4"""
import glob, json, os, re, subprocess, sys, textwrap

cikti, segs, hedef = sys.argv[1:4]
tl = json.load(open(os.path.join(cikti, "tl.json")))
sc = json.load(open(os.path.join(cikti, "sahneler.json")))
FPS, total = tl["fps"], tl["total"]
parca = sorted(glob.glob(os.path.join(segs, "seg_*.mp4")), key=lambda p: int(re.findall(r"seg_(\d+)", p)[0]))
if not parca:
    raise SystemExit("HATA: hiç video parçası yok")
liste = os.path.join(cikti, "liste.txt")
open(liste, "w").write("".join("file '%s'\n" % os.path.abspath(p) for p in parca))
sessiz = os.path.join(cikti, "sessiz.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste, "-c", "copy", sessiz], check=True)
kare = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                    "stream=nb_read_frames", "-of", "csv=p=0", sessiz]).decode().strip())
beklenen = len(tl["env"])
if kare != beklenen:
    raise SystemExit("HATA: kare sayısı %d, beklenen %d (eksik parça olabilir)" % (kare, beklenen))
# altyazı (DejaVu Bold Türkçe karakterleri destekler)
font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
vf = ["scale=1080:1920:flags=lanczos", "fps=30"]
for i, (s, e) in enumerate(zip(sc, tl["tl"])):
    f = os.path.join(cikti, "alt%02d.txt" % i)
    open(f, "w", encoding="utf-8").write("\n".join(textwrap.wrap(s["metin"], 24)))
    vf.append("drawtext=fontfile=%s:textfile=%s:fontsize=64:fontcolor=white:borderw=6:bordercolor=black:x=(w-text_w)/2:y=h*0.80:"
              "enable='between(t,%.2f,%.2f)'" % (font, f, e["t0"] - 0.05, e["t0"] + e["d"] + 0.15))
muzik = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "varliklar", "muzik1.mp3")
fc = ("[0:v]%s[v];[1:a]volume=1.5[ses];[2:a]volume=0.2,aloop=loop=-1:size=2e9,atrim=0:%.2f[m];"
      "[m][ses]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[d];[d][ses]amix=inputs=2:normalize=0:duration=first,"
      "alimiter=limit=0.95[a]") % (",".join(vf), total)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sessiz, "-i", os.path.join(cikti, "voice.wav"), "-i", muzik, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-t", "%.2f" % total, "-movflags", "+faststart", hedef], check=True)
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", hedef]))
boyut = os.path.getsize(hedef) / 1e6
ls = subprocess.run(["ffmpeg", "-nostats", "-i", hedef, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", ls)
agiz = sum(1 for x in tl["env"] if x > .15)
print("GERÇEK ÖLÇÜMLER")
print("video: %.1f sn, %.1f MB, 1080x1920, %d kare (12 fps çizim, 30 fps çıkış)" % (dur, boyut, kare))
print("sahne sayısı: %d | altyazı satırı: %d" % (len(sc), len(sc)))
print("ses: Piper tr_TR-dfki-medium | ses seviyesi: %s LUFS" % (lufs[-1] if lufs else "?"))
print("ağız hareketi karesi: %d/%d (sese bağlı)" % (agiz, len(tl["env"])))
