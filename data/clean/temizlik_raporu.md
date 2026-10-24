# Veri temizleme raporu

Üretim: `python ml/clean.py` — tohum (seed) 42

## Adım adım

| Veri | Adım | Önce | Sonra | Elenen | Açıklama |
|---|---|---:|---:|---:|---|
| GBIF | 1. Yinelenen gbifID | 1324 | 1224 | 100 | Aynı kayıt birden çok sayfada |
| GBIF | 2. 'Yok' (ABSENT) kayıtlar | 1224 | 1224 | 0 | Türün bulunmadığını bildiren kayıtlar |
| GBIF | 3. Tür düzeyine indirgeme | 1224 | 1092 | 132 | Cins veya üstü düzeyde tanımlanan kayıtlar |
| GBIF | 4. Koordinat aykırı değerleri | 1092 | 1092 | 0 | Türkiye dışı, 0/0 veya ters girilmiş koordinatlar |
| GBIF | 5. Aynı tür-yer-gün kopyaları | 1092 | 846 | 246 | Aynı gözlemin farklı veri setlerindeki kopyası |
| GBIF | 6. İl adı normalizasyonu | 846 | 846 | 0 | 54 farklı yazım -> 53 il; Kastamonu yazımları: 'Kastamonu'; Kastamonu kaydı: 129 |
| iNat | 1. Yinelenen photo_id | 16132 | 15576 | 556 | Aynı fotoğraf birden fazla sorguda gelmiş |
| iNat | 1b. Rehber dışı sınıflar | 15576 | 15576 | 0 | Kastamonu/Karadeniz'de GBIF kaydı olmadığı için rehberden çıkarılan türler |
| iNat | 2. Lisans filtresi | 15576 | 15576 | 0 | Yalnızca CC lisanslı fotoğraflar |
| iNat | 3. Eksik URL | 15576 | 15576 | 0 | Fotoğraf adresi olmayan kayıtlar |
| iNat | 4. Taksonomi normalizasyonu | 15576 | 15363 | 213 | Alt tür/varyete -> tür; sınıfla uyuşmayanlar atıldı |
| iNat | 5. Bozuk / inmemiş görüntü | 15363 | 15363 | 0 | Açılamayan veya indirilemeyen dosyalar |
| iNat | 6. Boyut / en-boy aykırı değer | 15363 | 15363 | 0 | Kısa kenar < 128px veya en/boy > 3.0 |
| iNat | 7. Birebir kopya (aynı dHash) | 15363 | 15344 | 19 | Farklı kimlikle yüklenmiş aynı fotoğraf |
| iNat | 8. Neredeyse kopya (Hamming<=4) | 15344 | 15323 | 21 | Kırpılmış/sıkıştırılmış kopyalar (train-test sızıntısını önler) |
| iNat | 9. Tarih / konum ayrıştırma | 15323 | 15323 | 0 | Ay bilinmeyen: 0, konum bilinmeyen: 0 (atılmadı) |
| iNat | 10. Sınıf dengeleme | 15323 | 12057 | 3266 | Sınıf başına en fazla 450; < 60 örnekli sınıflar çıkarıldı: yok |

## Model veri seti (sınıf × ayrım)

| Sınıf | train | val | test | toplam | gözlem |
|---|---:|---:|---:|---:|---:|
| Agaricus campestris | 319 | 68 | 63 | 450 | 265 |
| Agaricus xanthodermus | 311 | 72 | 67 | 450 | 270 |
| Amanita caesarea | 317 | 66 | 66 | 449 | 321 |
| Amanita muscaria | 317 | 69 | 64 | 450 | 325 |
| Amanita pantherina | 308 | 73 | 68 | 449 | 311 |
| Amanita phalloides | 321 | 66 | 63 | 450 | 280 |
| Amanita rubescens | 316 | 70 | 64 | 450 | 284 |
| Armillaria mellea | 321 | 64 | 65 | 450 | 283 |
| Boletus edulis | 317 | 68 | 64 | 449 | 310 |
| Cantharellus cibarius | 317 | 66 | 67 | 450 | 318 |
| Coprinus comatus | 318 | 70 | 62 | 450 | 332 |
| Craterellus cornucopioides | 319 | 65 | 66 | 450 | 315 |
| Entoloma sinuatum | 192 | 40 | 37 | 269 | 177 |
| Galerina marginata | 313 | 68 | 69 | 450 | 262 |
| Grifola frondosa | 308 | 75 | 67 | 450 | 298 |
| Gyromitra esculenta | 321 | 65 | 63 | 449 | 322 |
| Hydnum repandum | 315 | 67 | 68 | 450 | 274 |
| Hypholoma fasciculare | 313 | 69 | 68 | 450 | 299 |
| Lactarius deliciosus | 313 | 66 | 70 | 449 | 295 |
| Lepiota brunneoincarnata | 90 | 19 | 21 | 130 | 81 |
| Macrolepiota procera | 318 | 64 | 68 | 450 | 312 |
| Marasmius oreades | 315 | 65 | 69 | 449 | 293 |
| Morchella esculenta | 316 | 69 | 64 | 449 | 331 |
| Omphalotus olearius | 315 | 64 | 71 | 450 | 289 |
| Pleurotus ostreatus | 298 | 62 | 64 | 424 | 254 |
| Ramaria spp. | 306 | 69 | 66 | 441 | 293 |
| Rubroboletus satanas | 313 | 69 | 68 | 450 | 281 |
| mantar_degil | 315 | 68 | 67 | 450 | 450 |

Çıkarılan sınıflar (< 60 örnek): yok
Türkiye'den gelen fotoğraf: 543 / 12057

Sızıntı kontrolü (her gözlem yalnızca bir ayrımda): ✅ geçti

## GBIF — rehberdeki türler

| Tür | Türkiye | Kastamonu |
|---|---:|---:|
| *Amanita phalloides* | 25 | 2 |
| *Galerina marginata* | 7 | 1 |
| *Lepiota brunneoincarnata* | 1 | 0 |
| *Amanita muscaria* | 58 | 3 |
| *Amanita pantherina* | 45 | 2 |
| *Gyromitra esculenta* | 18 | 0 |
| *Omphalotus olearius* | 12 | 0 |
| *Entoloma sinuatum* | 3 | 0 |
| *Hypholoma fasciculare* | 37 | 1 |
| *Rubroboletus satanas* | 2 | 0 |
| *Amanita rubescens* | 33 | 0 |
| *Agaricus xanthodermus* | 6 | 0 |
| *Morchella esculenta* | 11 | 0 |
| *Armillaria mellea* | 35 | 0 |
| *Agaricus campestris* | 10 | 0 |
| *Boletus edulis* | 13 | 0 |
| *Cantharellus cibarius* | 14 | 1 |
| *Lactarius deliciosus* | 36 | 1 |
| *Macrolepiota procera* | 48 | 3 |
| *Amanita caesarea* | 44 | 0 |
| *Hydnum repandum* | 9 | 0 |
| *Craterellus cornucopioides* | 16 | 0 |
| *Pleurotus ostreatus* | 37 | 0 |
| *Coprinus comatus* | 129 | 0 |
| *Marasmius oreades* | 10 | 0 |
| *Ramaria spp.* | 7 | 0 |
| *Grifola frondosa* | 0 | 0 |

## Kastamonu'da en çok kaydı olan 25 tür (GBIF, toplam 129 kayıt)

| Tür | Kayıt | Rehberde |
|---|---:|:---:|
| *Clavariadelphus truncatus* | 4 |  |
| *Toniniopsis subincompta* | 4 |  |
| *Amanita muscaria* | 3 | ✅ |
| *Macrolepiota procera* | 3 | ✅ |
| *Xanthoria parietina* | 3 |  |
| *Gomphidius glutinosus* | 3 |  |
| *Geastrum triplex* | 3 |  |
| *Zyzygomyces bachmannii* | 3 |  |
| *Amanita phalloides* | 2 | ✅ |
| *Amanita pantherina* | 2 | ✅ |
| *Geopyxis foetida* | 2 |  |
| *Hygrophorus chrysodon* | 2 |  |
| *Calocera viscosa* | 2 |  |
| *Epicladonia stenospora* | 2 |  |
| *Flavoplaca flavocitrina* | 2 |  |
| *Rufoplaca subpallida* | 2 |  |
| *Blastenia crenularia* | 2 |  |
| *Bryoria fuscescens* | 2 |  |
| *Galerina marginata* | 1 | ✅ |
| *Hypholoma fasciculare* | 1 | ✅ |
| *Cantharellus cibarius* | 1 | ✅ |
| *Lactarius deliciosus* | 1 | ✅ |
| *Evernia prunastri* | 1 |  |
| *Bjerkandera adusta* | 1 |  |
| *Aleuria aurantia* | 1 |  |
