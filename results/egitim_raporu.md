# Model eğitim raporu

**Model:** EfficientNet-B0 (ImageNet ön eğitimli, transfer öğrenme) · **28 sınıf** · train 8462 / val 1816 / test 1779 fotoğraf

## Genel başarı (test seti — eğitimde hiç görülmedi)

| Metrik | Değer |
|---|---:|
| Top-1 doğruluk | 89.7% |
| Top-5 doğruluk | 98.2% |
| Makro recall | 89.0% |
| Kalibrasyon hatası (ECE) ham → kalibre | 0.114 → 0.016 (T=0.68) |

## Güvenlik metrikleri (model + karar katmanı birlikte)

| Metrik | Değer | Hedef |
|---|---:|---|
| Ölümcül/zehirli tür fotoğrafının KIRMIZI gösterilme oranı | 98.8% | yüksek |
| Ölümcül tür fotoğrafının KIRMIZI gösterilme oranı | 100.0% | yüksek |
| **Tehlikeli karışıklık** (zehirli → 'düşük riskli aday') | **0.5%** | ≈ 0 |
| Zehirli tür fotoğrafının 'mantar değil' sayılması | 0.0% | ≈ 0 |
| Mantar olmayan fotoğrafların reddedilmesi | 89.6% | yüksek |
| Düşük riskli türlerde GRİ sonuç (gereksiz alarm olmaması) | 85.8% | — |

### Gerçek risk → uygulamanın kararı (adet)

| Gerçek risk | KIRMIZI | SARI | GRI | MANTAR_DEGIL |
|---|---:|---:|---:|---:|
| olumcul | 153 | 0 | 0 | 0 |
| yuksek | 432 | 4 | 3 | 0 |
| orta | 51 | 255 | 17 | 3 |
| dusuk | 83 | 29 | 681 | 1 |
| mantar_degil | 6 | 1 | 0 | 60 |

![güvenlik](guvenlik_matrisi.png)

## Sınıf bazında recall (test)

| Sınıf | Risk | Recall |
|---|---|---:|
| *Agaricus campestris* | dusuk | 79.4% |
| *Agaricus xanthodermus* | orta | 76.1% |
| *Amanita caesarea* | dusuk | 90.9% |
| *Amanita muscaria* | yuksek | 92.2% |
| *Amanita pantherina* | yuksek | 82.4% |
| *Amanita phalloides* | olumcul | 88.9% |
| *Amanita rubescens* | orta | 78.1% |
| *Armillaria mellea* | orta | 72.3% |
| *Boletus edulis* | dusuk | 84.4% |
| *Cantharellus cibarius* | dusuk | 98.5% |
| *Coprinus comatus* | dusuk | 95.2% |
| *Craterellus cornucopioides* | dusuk | 95.5% |
| *Entoloma sinuatum* | yuksek | 83.8% |
| *Galerina marginata* | olumcul | 94.2% |
| *Grifola frondosa* | dusuk | 97.0% |
| *Gyromitra esculenta* | yuksek | 98.4% |
| *Hydnum repandum* | dusuk | 86.8% |
| *Hypholoma fasciculare* | yuksek | 83.8% |
| *Lactarius deliciosus* | dusuk | 95.7% |
| *Lepiota brunneoincarnata* | olumcul | 66.7% |
| *Macrolepiota procera* | dusuk | 92.6% |
| *Marasmius oreades* | dusuk | 92.8% |
| *Morchella esculenta* | orta | 98.4% |
| *Omphalotus olearius* | yuksek | 95.8% |
| *Pleurotus ostreatus* | dusuk | 87.5% |
| *Ramaria spp.* | orta | 98.5% |
| *Rubroboletus satanas* | yuksek | 95.6% |
| *mantar_degil* | — | 91.0% |

![eğriler](egitim_egrileri.png)

![karışıklık](karisiklik_matrisi.png)

ONNX dışa aktarma doğrulaması: PyTorch ile en büyük çıktı farkı 1.57e-05.
