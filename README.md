# 🍄 MycoGuard — Mantar Zehirlenme Risk Uyarı Sistemi

> **Konsept prototip (hackathon).** Model çıktıları **simüledir**; karar mantığı ve arayüz **gerçekten çalışır**.
> MycoGuard **hiçbir mantarın yenilebilir olduğunu söylemez.** Yeme kararı için mutlaka uzman onayı gerekir.

## Problem
Her sonbahar ve ilkbaharda mantar zehirlenmeleri artıyor. İnsanlar mantarı fotoğraftan tanımaya çalışıyor ve yanlış tanıyor. Ölümcül türlerde belirtiler saatler, hatta günler sonra başlıyor.

## Çözüm
Kullanıcı mantarın fotoğrafını çeker → sistem **ilk 5 aday türü**, **zehirlenme risk seviyesini**, ölümcül **ikiz türleri**, habitatı ve mevsimi gösterir → risk varsa net uyarı ve acil durum yönlendirmesi verir.

**Konumlandırma:** "Mantar yenilebilir mi?" uygulaması değil, **zehirlenme riskini azaltan uyarı sistemi**.

| Seviye | Koşul | Mesaj |
|---|---|---|
| 🔴 KIRMIZI | Adaylarda ≥%5 olasılıklı ölümcül/yüksek riskli tür var | "Tehlikeli aday var. Yeme." |
| 🟡 SARI | Birinci aday <%60 ya da şartlı (orta riskli) tür | "Belirsiz. Yeni fotoğraf çek / uzmana göster." |
| ⚪ GRİ | Düşük riskli aday, belirsizlik yok | "Düşük riskli aday. Yeme kararı için uzman onayı gerekir." |
| ⛔ MANTAR DEĞİL | Fotoğraf mantar gibi görünmüyor | "Mantar fotoğrafı yükle." |

Bilerek **yeşil renk yok**, **"güvenli" etiketi yok**.

## Nasıl çalıştırılır

**Arayüz:** `app/index.html` dosyasını tarayıcıda açın (çift tıklama yeterli, internet gerekmez).

**Karar katmanı testi** (Python 3, bağımlılık yok):

```bash
python src/decide.py
```

Beklenen çıktı: `8/8 senaryo OK`.

**Veriyi değiştirdiyseniz** arayüz verisini yeniden üretin:

```bash
python src/build_app_data.py
```

## Neyin simüle olduğu

| Parça | Prototipte | Gerçek üründe |
|---|---|---|
| Fotoğraf → tür olasılıkları | ⚠️ **Simüle** (`data/demo_cases.json`) | Eğitilmiş görüntü modeli |
| "Mantar mı?" kontrolü | ⚠️ **Simüle** (`mantar_olma_olasiligi`) | Ayrı ikili sınıflandırıcı |
| Tür bilgi tablosu | ✅ Gerçek yapı, **taslak içerik** (`data/species_info.csv`) | Uzman onaylı, kaynaklı tablo |
| Karar katmanı (eşikler, en kötü aday kuralı) | ✅ **Gerçekten çalışır** (`src/decide.py`, `app/index.html`) | Aynı mantık, kalibre edilmiş modelle |
| Risk seviyeleri ve uyarı arayüzü | ✅ **Gerçekten çalışır** | Aynı |
| İkiz tür kartları | ✅ Tablodan gelir | Aynı |
| Acil durum ekranı | ✅ Statik içerik | Resmî kaynaklarla doğrulanmış |

## Demo senaryoları

| # | Senaryo | Seviye | Neyi gösteriyor |
|---|---|---|---|
| c1 | Çayır mantarı + *Amanita phalloides* | 🔴 | Birinci tahmin zararsız görünse de ikiz uyarısı |
| c2 | *A. phalloides* %91 | 🔴 | Ölümcül tür + gecikmeli belirti uyarısı |
| c3 | Horoz mantarı + *Omphalotus* | 🔴 | Güven eşiği geçilse bile ikiz uyarısı |
| c4 | Kuzugöbeği + *Gyromitra* | 🔴 | "Kesilince içi boş mu?" ayırt edici ipucu |
| c5 | Bulanık fotoğraf | 🟡 | "Emin değilim" + yeni fotoğraf isteme |
| c6 | Kozalak fotoğrafı | ⛔ | Mantar olmayan girdiyi reddetme |
| c7 | *Marasmius oreades* + *Clitocybe rivulosa* | 🔴 | Aynı çayırda gerçekçi karışıklık |
| c8 | *Pleurotus ostreatus* %88 | ⚪ | "Güvenli" demeden düşük riskli aday gösterme |

## Mimari

```
Fotoğraf → [1] Mantar mı? ──hayır──► ⛔
              │evet
              ▼
           [2] Görüntü modeli → top-5     (prototipte SİMÜLE)
              ▼
           [3] Karar katmanı (kural)      (GERÇEK)
              ▼
           [4] species_info.csv eşleşmesi (GERÇEK)
              ▼
           Sonuç ekranı + uyarı bandı + acil durum butonu
```

## Veri stratejisi (gerçek ürün)
4 katman: görüntü verisi (FungiTastic, Danish Fungi 2020, iNaturalist, GBIF), uzman onaylı bilgi tabanı, Türkiye saha verisi ve eğitime hiç girmeyen **altın test seti**. Ayrıntı: [`docs/proje-plani.md`](docs/proje-plani.md) bölüm 4, kaynak ve lisanslar: [`docs/veri-kaynaklari.md`](docs/veri-kaynaklari.md).

## Repo yapısı

```
├── app/index.html          # prototip arayüz (app/data.js otomatik üretilir)
├── data/species_info.csv   # 20 türlük TASLAK bilgi tablosu
├── data/demo_cases.json    # 8 simüle senaryo + eşikler
├── src/decide.py           # karar katmanı + senaryo testi
├── src/build_app_data.py   # data/ → app/data.js
└── docs/                   # plan, veri kaynakları, güvenlik-etik, günlük
```

## Sınırlılıklar ve sorumluluk reddi
- Bu bir **konsept prototiptir**; gerçek bir görüntü modeli içermez ve hiçbir doğruluk iddiasında bulunmaz.
- `species_info.csv` içeriği **taslaktır** ve henüz kaynaklarla doğrulanmamıştır.
- Acil durum numaraları (114, 112) sunumdan önce resmî kaynaklardan doğrulanacaktır.
- MycoGuard bir uzman veya hekim yerine geçmez. **Hiçbir sonuç yeme onayı değildir.**

## Takım

| Rol | Kişi | Sorumluluk |
|---|---|---|
| Küratör | _TBD_ | `species_info.csv` doğrulama, kaynaklar, ikiz türler |
| Arayüz | _TBD_ | `app/index.html`, seviye ve acil durum ekranları |
| Karar katmanı ve test | _TBD_ | `src/decide.py`, senaryo testleri, (ops.) Colab mini model |
| Sunum ve GitHub | _TBD_ | README, günlük, demo videosu, slaytlar |

## Lisans
Kod: MIT (bkz. `LICENSE`). Üçüncü taraf veri setleri kendi lisanslarına tabidir; bkz. `docs/veri-kaynaklari.md`.
