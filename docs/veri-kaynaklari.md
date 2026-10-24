# Veri kaynakları

Her kaynağın linki, lisansı ve kontrol tarihi burada tutulur. **Lisans sütunu "DOĞRULANACAK" olan hiçbir kaynak gerçek eğitimde kullanılmaz.**

| Kaynak | Link | İçerik | Rolü | Lisans | Kontrol tarihi | Kontrol eden |
|---|---|---|---|---|---|---|
| FungiTastic (CVPRW 2025) | https://bohemianvra.github.io/FungiTastic · Kaggle `picekl/fungitastic` · arXiv 2408.13632 | ~350 bin gözlem, ~6 bin tür, metadata, maskeler, kısmen DNA doğrulamalı test | Ana kaynak (önce Mini alt kümesi) | DOĞRULANACAK | — | — |
| Danish Fungi 2020 (WACV 2022) | https://sites.google.com/view/danish-fungi-dataset · arXiv 2103.10107 | 1.604 tür, ~248 bin eğitim görüntüsü, uzman etiketli | İkinci ana kaynak (mini / 300px sürüm) | DOĞRULANACAK (bazı ilişkili kaynaklarda CC BY-NC 4.0 belirtiliyor — ticari kullanım yok) | — | — |
| iNaturalist (araştırma düzeyi) | https://www.inaturalist.org | Topluluk doğrulamalı gözlemler | Türkiye gözlemleri | Görüntü başına (yalnızca CC lisanslılar) | — | — |
| GBIF | https://www.gbif.org | Tür görülme kayıtları | Türkiye tür listesi, habitat/mevsim istatistiği | Kayıt/medya başına | — | — |
| Kaggle `thehir0/mushroom-species` | https://www.kaggle.com/datasets/thehir0/mushroom-species | 100 tür, 50 bin+ fotoğraf (Rusya) | Yardımcı / hızlı baseline | DOĞRULANACAK | — | — |
| UCI Mushroom | https://www.kaggle.com/datasets/uciml/mushroom-classification | Tablo tabanlı, 1981 rehberinden hipotetik örnekler | Kullanılmayacak (gerçek dünya başarısı göstermez) | — | — | — |
| FungiCLEF 2023 | https://www.imageclef.org/FungiCLEF2023 | Yarışma, değerlendirme protokolü | Metrik/protokol referansı | — | — | — |

## species_info.csv içerik kaynakları

Her satır en az bir akademik/resmî kaynakla doğrulanınca `dogrulama_durumu = DOGRULANDI` ve `kaynak` sütununa link yazılır.

Önerilen kaynaklar: Sağlık Bakanlığı / Ulusal Zehir Danışma Merkezi (UZEM) yayınları, üniversite mikoloji makaleleri, GBIF Türkiye kayıtları.

| Tür grubu | Sorumlu | Durum |
|---|---|---|
| s01–s05 | _TBD_ | Bekliyor |
| s06–s10 | _TBD_ | Bekliyor |
| s11–s15 | _TBD_ | Bekliyor |
| s16–s20 | _TBD_ | Bekliyor |

## Veri kalite kontrol listesi (gerçek veri aşaması)
- [ ] Görüntü hash'iyle yinelenenleri temizle (train/test sızıntısını önle)
- [ ] Bölmeyi **gözlem kimliğine göre** yap
- [ ] Her kaynağın lisansını bu dosyaya yaz
- [ ] Rastgele 100 görüntünün etiketini elle kontrol et
- [ ] "Mantar değil" sınıfı için negatif örnekler topla (taş, kozalak, çiçek, ağaç kabuğu)
- [ ] Ayrı bir "bilinmeyen tür" test kümesi hazırla
