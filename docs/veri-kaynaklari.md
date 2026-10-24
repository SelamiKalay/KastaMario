# Veri kaynakları ve lisanslar

## Kullanılan kaynaklar

| Kaynak | Link | Ne alındı | Lisans | Erişim |
|---|---|---|---|---|
| iNaturalist (araştırma düzeyi gözlemler) | https://www.inaturalist.org · API v1 | 28 tür + "mantar değil" sınıfı için fotoğraf ve gözlem bilgileri (`ml/collect.py`) | Fotoğraf başına CC0 / CC BY / CC BY-SA / CC BY-NC / CC BY-NC-SA / CC BY-ND / CC BY-NC-ND — "tüm hakları saklı" fotoğraflar indirilmez ve temizlikte de elenir | Ekim 2026 |
| GBIF | https://www.gbif.org · Occurrence API | Rehberdeki türlerin Türkiye kayıtları, Kastamonu çevresindeki mantar kayıtları | Kayıt başına CC0 / CC BY / CC BY-NC (veri setine göre) | Ekim 2026 |
| Gemma 4 E4B | https://huggingface.co/google/gemma-4-E4B-it | Görsel-dil modeli (Ollama: `gemma4:e4b`) | [Apache 2.0](https://ai.google.dev/gemma/docs/gemma_4_license) | Ekim 2026 |
| EfficientNet-B0 (ImageNet) | https://pytorch.org/vision | Transfer öğrenme başlangıç ağırlıkları | BSD-3 | Ekim 2026 |

Atıflar: rehberde gösterilen her fotoğrafın sahibi ve lisansı `data/clean/thumbs.json` içinde ve uygulamada fotoğrafın üzerinde yazılıdır. Eğitimde kullanılan tüm fotoğrafların atıf ve lisansı `data/clean/inat_clean.csv` içindedir.

> Lisans notu: CC BY-NC lisanslı fotoğraflar ticari olmayan kullanım içindir. Ticari bir sürümde eğitim seti yalnızca CC0 / CC BY / CC BY-SA ile yeniden üretilmelidir (`ml/clean.py` içinde `ALLOWED_LICENSES`).

## İncelenen, gelecek sürüm için aday kaynaklar

| Kaynak | Link | Not |
|---|---|---|
| FungiTastic (CVPRW 2025) | https://bohemianvra.github.io/FungiTastic · Kaggle `picekl/fungitastic` | ~350 bin gözlem, kısmen DNA doğrulamalı test seti |
| Danish Fungi 2020 (WACV 2022) | https://sites.google.com/view/danish-fungi-dataset | Uzman etiketli; ilişkili kaynaklarda CC BY-NC 4.0 |
| FungiCLEF | https://www.imageclef.org | Değerlendirme protokolü referansı |

## Veri kalite kontrol listesi
- [x] Görüntü hash'iyle (dHash) birebir ve neredeyse kopyaları temizle
- [x] Bölmeyi **gözlem kimliğine göre** yap (aynı mantarın fotoğrafları aynı tarafta)
- [x] Her kaynağın lisansını bu dosyaya yaz
- [x] "Mantar değil" sınıfı için negatif örnekler (bitki, çam, yosun, böcek)
- [ ] Rastgele 100 görüntünün etiketini elle kontrol et
- [ ] Türkiye'den uzman doğrulamalı "altın test seti" (üniversite mikoloji bölümleriyle)
