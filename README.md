# cocuk-animasyon

Türkçe hikâyeden otomatik 3D çocuk animasyonu (MP4) üreten sistem. **Durum: ilk çalışan sürüm geliştiriliyor.**

## Gerçekte çalışan zincir
hikâye metni → kural tabanlı sahne ayrıştırma (`uretim/hikaye_sahne.py`) → Piper Türkçe seslendirme (`uretim/plan.py`)
→ Blender (Cycles, CPU) 3D render (`uretim/render.py`) → FFmpeg birleştirme + altyazı + müzik (`uretim/birlestir.py`)
→ GitHub Release'e MP4. Hepsi **GitHub Actions** üzerinde (`.github/workflows/uret.yml`), ücretsiz.

## Sınırlar (dürüst liste)
- Sahne ayrıştırma **kural tabanlıdır**, yapay zekâ modeli değildir; yalnızca sınırlı kelimeleri tanır (yatak, sepet, kanepe, selam, düşün, sarıl, dans...).
- Karakter oyuncak tarzı 3D'dir (gerçekçi insan değil). Tek karakter (Pırpır) + ayıcık, tek oda.
- Seslendirme tek bir Piper modeliyle (`tr_TR-dfki-medium`, erkek sesi) yapılır.
- Render CPU'dadır: 30 sn video yaklaşık 15-30 dk sürer. GitHub ücretsiz kotası (özel depoda 2000 dk/ay, herkese açık depoda sınırsız ama eşzamanlı iş sayısı sınırlı) geçerlidir.
- Mixamo otomatikleştirilemez (Adobe girişi, API yok), kullanılmıyor. MakeHuman şu an kullanılmıyor.
- Google Colab otomatik çalıştırılamaz; kullanılmıyor.

## Lisanslar
Blender GPL (çıktı sizindir) • Piper MIT (modeller: kendi lisansları, `tr_TR-dfki` için model kartına bakın) • FFmpeg LGPL/GPL •
Müzik: Mixkit "Feeling Happy" (Mixkit ücretsiz lisansı) • Yazı tipi: DejaVu (özgür).
