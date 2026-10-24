# Veri temizleme raporu

Üretim: `python ml/clean.py` — tohum (seed) 42

## Adım adım

| Veri | Adım | Önce | Sonra | Elenen | Açıklama |
|---|---|---:|---:|---:|---|
| GBIF | 1. Yinelenen gbifID | 1268 | 1168 | 100 | Aynı kayıt birden çok sayfada |
| GBIF | 2. 'Yok' (ABSENT) kayıtlar | 1168 | 1168 | 0 | Türün bulunmadığını bildiren kayıtlar |
| GBIF | 3. Tür düzeyine indirgeme | 1168 | 1044 | 124 | Cins veya üstü düzeyde tanımlanan kayıtlar |
| GBIF | 4. Koordinat aykırı değerleri | 1044 | 1044 | 0 | Türkiye dışı, 0/0 veya ters girilmiş koordinatlar |
| GBIF | 5. Aynı tür-yer-gün kopyaları | 1044 | 839 | 205 | Aynı gözlemin farklı veri setlerindeki kopyası |
| GBIF | 6. İl adı normalizasyonu | 839 | 839 | 0 | 53 farklı yazım -> 52 il; Kastamonu yazımları: 'Kastamonu'; Kastamonu kaydı: 129 |

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
