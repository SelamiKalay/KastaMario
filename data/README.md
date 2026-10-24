# data/

| Dosya | İçerik |
|---|---|
| `species_info.csv` | 25 türlük bilgi tabanı: risk, zehir notu, belirtiler, belirti başlangıcı (saat), ilk yardım, habitat, Kastamonu notu, boy, yetişme süreci, aylar, toplama notu, ikiz türler, ayırt edici ipucu. `dusuk` risk "güvenli" demek değildir. |
| `demo_cases.json` | Karar eşikleri + 8 örnek vaka (uygulamadaki "Örnek vakalar" ve testler). |
| `clean/` | `ml/clean.py` çıktıları: temiz eğitim listesi, temiz GBIF kayıtları, tür istatistikleri, temizlik raporu, rehber fotoğraf atıfları. |
| `raw/` | `ml/collect.py` ham indirmeleri (repoya girmez, `.gitignore`). |

Bilgi tabanı genel mikoloji literatürüne ve GBIF Türkiye kayıtlarına dayanır; her satır uzman incelemesinden geçirilmektedir (`dogrulama_durumu` sütunu).

Değişiklikten sonra: `python -m pytest -q` ve `python src/build_app_data.py`.

## Ham veriyi yeniden indirmek

```bash
python ml/collect.py            # iNaturalist + GBIF
python ml/collect.py --only gbif
```

- **iNaturalist:** her tür için Avrupa + Türkiye'den en fazla 400 araştırma düzeyi gözlem, gözlem başına 2 fotoğraf, yalnızca CC lisanslı; "mantar değil" sınıfı için Türkiye'den bitki, çam, yosun ve böcek fotoğrafları.
- **GBIF:** rehberdeki her türün Türkiye kayıtları + Kastamonu çevresindeki (koordinat kutusu ve il adı) tüm mantar kayıtları.

## Hangi türler rehberde?
Rehber yalnızca **Kastamonu'nun bulunduğu Karadeniz kuşağında** (enlem ≥ 40,5) GBIF gözlem kaydı olan türleri içerir. İlk listedeki 28 türden *Amanita virosa*, *Cortinarius orellanus* ve *Clitocybe rivulosa* Türkiye'de hiç GBIF kaydı bulunmadığı için çıkarıldı. Kastamonu iline ait kayıtlar çok seyrek olduğundan (rehberdeki türlerin yalnızca 8'inde kayıt var) il sınırı yerine bölge ölçütü kullanıldı; kaydın olmaması türün bulunmadığını kanıtlamaz. Kastamonu kayıtlarının önemli bir kısmı likenlere (Xanthoria, Bryoria, Evernia…) aittir; likenler biyolojik olarak mantardır ancak rehberin kapsamı dışındadır.
