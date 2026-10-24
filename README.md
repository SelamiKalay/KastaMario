# 🍄 MycoGuard Kastamonu

**Yapay zekâ destekli mantar zehirlenme risk rehberi.** Mantarın fotoğrafını çekin; MycoGuard olası türleri, zehirlenme riskini, ölümcül ikiz türleri, belirtilerin kaç saatte başladığını, yediyseniz ne yapmanız gerektiğini, mantarın nerede ve ne zaman yetiştiğini gösterir. Kastamonu ormanları (Küre Dağları, Ilgaz, kıyı kestane-meşe ormanları) için hazırlanmıştır.

> MycoGuard **hiçbir mantarın yenilebilir olduğunu söylemez.** Zehirliyi yenilebilir sanmak ölümcül olabilir; yenilebiliri zehirli sanmak en fazla boş sepettir. Bu asimetri tasarımın temelidir.

## Yapay zekâ ne yapıyor?

MycoGuard iki açık modeli ve kural tabanlı bir güvenlik katmanını birlikte kullanır:

| Katman | Model | Lisans | Görevi |
|---|---|---|---|
| 1. Görüntü sınıflandırıcı | **EfficientNet-B0**, bu projede iNaturalist fotoğraflarıyla eğitildi (`ml/train.py`) | Kod MIT; ön eğitimli ağırlıklar [torchvision (BSD-3)](https://github.com/pytorch/vision/blob/main/LICENSE) | Fotoğraftan tür olasılıkları + "mantar değil" tespiti. ONNX olarak **cihazda, internetsiz** çalışır. |
| 2. Görsel-dil modeli | **[Gemma 4 E4B](https://huggingface.co/google/gemma-4-E4B-it)** (Google DeepMind, açık ağırlıklı, ~4,5 milyar efektif parametre; küçük dil modeli) — [Ollama](https://ollama.com) ile yerel | [Apache 2.0 — Gemma 4 lisansı](https://ai.google.dev/gemma/docs/gemma_4_license) | Fotoğraftaki ayırt edici özellikleri **yapılandırılmış JSON** olarak çıkarır (sap tabanında torba, halka, lamel rengi, alt yüz tipi, substrat); bilgi tabanına dayalı Türkçe asistan. |
| 3. Güvenlik kuralları | — | MIT | **En kötü aday kuralı**: adaylardan biri ≥%5 ihtimalle ölümcül/zehirliyse sonuç KIRMIZI. Gemma bulguları riski **yalnızca yükseltebilir**, asla düşüremez. |

### Örnek: Gemma 4 riski nasıl yükseltir?
Görüntü modeli bir mantarı %70 "çayır mantarı" görür. Gemma 4 fotoğrafta **sap tabanında torba** tespit eder → kural katmanı sonucu **KIRMIZI**'ya çeker: *"Sap tabanında torba görünüyor. Bu, ölümcül köygöçüren grubunun en önemli işaretidir."*

```
Fotoğraf ─┬─► [1] EfficientNet-B0 (cihazda) ──► top-5 tür + mantar mı?
          │                                        │
          └─► [2] Gemma 4 E4B (Ollama) ──► görsel özellikler (JSON)
                                                   │
                     [3] Güvenlik kuralları ◄──────┘
                     • en kötü aday kuralı         → 🔴 Zehirli olabilir
                     • belirsizlik eşiği (%60)     → 🟡 Emin değiliz
                     • Gemma risk yükseltmesi      → ⚪ Düşük riskli aday (uzman onayı şart)
                                                   → ⛔ Mantar değil
                     ▼
     Sonuç + ikiz tür uyarıları + belirti süresi + ilk yardım + Kastamonu takvimi
```

## Özellikler
- 📷 **Tara:** fotoğraf → 3 adımlı yapay zekâ hattı → risk, en olası 5 tür, "bunu sakın karıştırma" kartları
- ✦ **Asistan (Gemma 4):** "Yedim ne yapmalıyım?", "Köygöçüreni yumurta mantarından nasıl ayırırım?" — yanıtlar yalnızca tür bilgi tabanına dayanır (RAG), yasak ifadeler süzülür
- 📖 **Rehber:** 25 tür — zehirlilik, belirtiler, etki süresi, ilk yardım, boy, yetişme süreci, Kastamonu notu, Türkiye gözlem kayıtları (GBIF)
- 📅 **Takvim:** Kastamonu'da hangi ay hangi türler çıkar; ölümcül türlerin dönemi vurgulanır
- 🚨 **Yedim!:** 114 / 112, belirti zaman çizelgesi (6 saatten geç başlayan belirti → ölümcül zehirlenme uyarısı)
- 📱 **Mobil:** PWA (ana ekrana eklenebilir, çevrimdışı çalışır); Capacitor ile Android/iOS paketine hazır

## Hızlı başlangıç

```bash
git clone https://github.com/SelamiKalay/BAKLAVA.git
cd BAKLAVA
```

**1. Gemma 4'ü kurun** ([Ollama](https://ollama.com/download)):

```bash
ollama pull gemma4:e4b
```

**2. Uygulamayı başlatın** (yalnızca Python 3.10+, ek paket gerekmez):

```bash
python server/app.py
```

Tarayıcıda `http://localhost:8000` adresini açın. Telefondan denemek için aynı ağdaki bilgisayarın IP adresini kullanın. Gemma çalışmıyorsa uygulama görüntü modeli + kurallarla çalışmaya devam eder.

Farklı model: `MYCOGUARD_GEMMA=gemma4:e2b python server/app.py`

## Veri ve model hattı (yeniden üretmek için)

```bash
pip install -r requirements-ml.txt
python ml/collect.py        # 1. ham veri: iNaturalist fotoğrafları + GBIF Türkiye kayıtları
python ml/clean.py          # 2. temizleme ve ayrıştırma -> data/clean/ + temizlik_raporu.md
python ml/train.py          # 3. EfficientNet-B0 eğitimi -> app/model/*.onnx + results/
python ml/thumbs.py         # rehber fotoğrafları (CC lisanslı, atıflı)
python src/build_app_data.py
```

**Veri temizleme adımları** (`ml/clean.py`, ayrıntı `data/clean/temizlik_raporu.md`): yinelenen kayıtlar, lisans filtresi (yalnızca CC), taksonomi normalizasyonu (alt tür/varyete → tür), bozuk/küçük/aykırı en-boy oranlı görseller, **algısal hash (dHash) ile birebir ve neredeyse kopya fotoğraflar**, tarih/konum ayrıştırma, sınıf dengeleme ve **gözlem kimliğine göre sızıntısız train/val/test ayrımı**. GBIF tarafında: ABSENT kayıtlar, tür düzeyine indirgeme, Türkiye dışı/0-0/ters koordinatlar, aynı tür-yer-gün kopyaları ve il adı normalizasyonu ("KASTAMONU", "Kastamonu İli", "Kastamonu Province" → `kastamonu`).

**Model sonuçları:** `results/egitim_raporu.md` — top-1/top-5 doğruluk, sınıf bazında recall, kalibrasyon (ECE) ve güvenlik metrikleri: zehirli tür → KIRMIZI oranı ve **tehlikeli karışıklık oranı** (zehirli bir mantarın "düşük riskli" gösterilmesi; hedef ≈ 0).

## Testler

```bash
python -m pytest -q
```

| Test dosyası | Ne doğrular |
|---|---|
| `tests/test_decide.py` | 8 örnek vaka, eşik sınırları, en kötü aday kuralı, her tehlikeli tür birinci adaysa KIRMIZI |
| `tests/test_species_table.py` | Tür tablosu şeması, aylar, belirti saatleri, ikiz türler, tehlikeli türler "Toplanmaz", "güvenli" ifadesi yasağı |
| `tests/test_parity.py` | Tarayıcıdaki `app/decide.js` ile `src/decide.py` 2000 rastgele vakada aynı kararı veriyor |
| `tests/test_gemma.py` | Gemma risk yükseltme kuralları, riskin asla düşmemesi, yasak ifade süzgeci, RAG bağlamı, Ollama yokken davranış |
| `tests/test_clean.py` | İl adı/tür adı/tarih/konum ayrıştırma, lisans filtresi, dHash kopya tespiti, sızıntısız ayırma, dengeleme |

## Proje yapısı

```
├── app/                  # Mobil uyumlu web uygulaması (PWA)
│   ├── index.html        #   arayüz
│   ├── decide.js         #   güvenlik kuralları (Python ile eşdeğer)
│   ├── model.js          #   cihazda ONNX çıkarımı (onnxruntime-web)
│   ├── model/            #   eğitilmiş model + etiketler
│   └── vendor/ort/       #   onnxruntime-web 1.20.1 (MIT)
├── server/               # Gemma 4 uç noktaları + statik sunucu (bağımlılıksız)
├── ml/                   # collect -> clean -> train -> thumbs
├── src/                  # karar katmanı (Python) + uygulama verisi üretimi
├── data/                 # species_info.csv, demo_cases.json, clean/ (raw/ repoya girmez)
├── results/              # eğitim raporu, metrikler, grafikler
├── tests/                # pytest
└── docs/                 # veri kaynakları, güvenlik-etik, günlük
```

## Bağımlılıklar ve lisanslar

| Bileşen | Lisans |
|---|---|
| MycoGuard kodu | MIT (`LICENSE`) |
| Gemma 4 E4B | [Apache 2.0](https://ai.google.dev/gemma/docs/gemma_4_license) |
| Ollama | [MIT](https://github.com/ollama/ollama/blob/main/LICENSE) |
| PyTorch / torchvision (EfficientNet-B0 ağırlıkları) | BSD-3 |
| onnxruntime-web 1.20.1 | MIT |
| iNaturalist fotoğrafları | Her fotoğrafın kendi CC lisansı; atıflar `data/clean/thumbs.json` ve `data/clean/inat_clean.csv` içinde |
| GBIF kayıtları | Kayıt başına CC0 / CC BY / CC BY-NC — bkz. `docs/veri-kaynaklari.md` |

## Sorumluluk reddi
MycoGuard bilgilendirme amaçlıdır; tıbbi tavsiye veya uzman tür tanımının yerine geçmez. Model hata yapabilir; bu yüzden güvenlik kuralları her zaman en kötü olasılığı esas alır. Mantar yediyseniz belirti beklemeden **112** veya **114**'ü (Ulusal Zehir Danışma Merkezi) arayın.
