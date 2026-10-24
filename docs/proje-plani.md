# 🍄 MycoGuard — Mantar Zehirlenme Risk Uyarı Sistemi
### Hackathon Konsept Prototip Planı (v2)

> **Son güncelleme:** 24 Ekim 2026
> **Kapsam kararı:** Bu hackathonda **tam çalışan uygulama yapmıyoruz**. Fikrin ön gösterimini (konsept prototip) yapıyoruz. Model çıktıları **simüle edilir**, ama **karar mantığı ve arayüz gerçekten çalışır**. Gerçek ürün için gerekli sağlam veri stratejisi ayrıca planlanır (bölüm 4).

**Bu pakette 3 dosya var:**

| Dosya | Ne işe yarar |
|---|---|
| `mantar-ai-proje-plani.md` | Bu plan |
| `species_info.csv` | 20 türlük demo bilgi tablosu (risk, habitat, mevsim, ikiz türler) |
| `demo_cases.json` | 8 hazır demo senaryosu (simüle edilmiş model çıktılarıyla) |

---

## 0. Güvenlik ilkesi (sunumun omurgası)

**Uygulama asla "bu mantar yenilebilir / güvenli" demez.** Zehirliyi yenilebilir sanmak ölümcül olabilir; yenilebiliri zehirli sanmak ise en fazla boş sepet demektir. Bu asimetri tasarımın temelidir.

| Yapma ❌ | Yap ✅ |
|---|---|
| "Bu mantar yenilebilir" | "X türüne benziyor. Yeme kararı için uzman onayı gerekir." |
| Tek tahmin göstermek | İlk 5 aday + olasılık |
| Emin değilken tahmin etmek | "Güvenilir tahmin yapılamadı" |
| Yeşil renk (güvenli çağrışımı) | Kırmızı / sarı / **gri** seviyeler (yeşil yok) |

**Üç seviyeli arayüz (+1 ret durumu):**

| Seviye | Koşul | Mesaj |
|---|---|---|
| 🔴 KIRMIZI | Adaylar arasında ölümcül/yüksek riskli tür var | "Tehlikeli aday var. Yeme." |
| 🟡 SARI | Birinci tahmin belirsiz (<%60) veya şartlı yenilebilir tür | "Belirsiz. Yeni fotoğraflar çek / uzmana göster." |
| ⚪ GRİ | Düşük riskli aday, belirsizlik yok | "Düşük riskli aday. Yeme kararı için uzman onayı gerekir." |
| ⛔ MANTAR DEĞİL | Fotoğraf mantar gibi görünmüyor | "Mantar fotoğrafı yükle." |

---

## 1. Proje özeti

**Problem:** Her sonbahar ve ilkbaharda mantar zehirlenmesi vakaları artıyor. İnsanlar mantarı fotoğraftan tanımaya çalışıyor ve yanlış tanıyor.

**Fikir:** Kullanıcı mantarın fotoğrafını çeker → sistem aday türleri, **zehirlenme risk seviyesini**, ölümcül ikiz türleri, yetiştiği ortamı ve mevsimi gösterir → risk varsa net uyarı ve acil durum yönlendirmesi verir.

**Konumlandırma:** "Mantarın yenilebilir olduğunu söyleyen uygulama" değil, **"zehirlenme riskini azaltan uyarı sistemi"**.

**Hedef kitle:** Doğa yürüyüşçüleri, kırsal bölge halkı, mantar toplayıcıları, aileler, okullar.

---

## 2. Prototipte ne gerçek, ne simüle?

Jüriye dürüst anlatacağımız ayrım (bu ayrımı açıkça söylemek puan getirir):

| Parça | Prototipte | Gerçek üründe |
|---|---|---|
| Fotoğraf → tür olasılıkları | ⚠️ **Simüle** (`demo_cases.json`) | Eğitilmiş görüntü modeli |
| "Mantar mı?" kontrolü | ⚠️ **Simüle** (`mantar_olma_olasiligi`) | Ayrı ikili sınıflandırıcı |
| Tür bilgi tablosu | ✅ Gerçek yapı, **taslak içerik** (`species_info.csv`) | Uzman onaylı, kaynaklı tablo |
| Karar katmanı (eşikler, en kötü aday kuralı) | ✅ **Gerçekten çalışır** | Aynı mantık, kalibre edilmiş modelle |
| Risk seviyeleri ve uyarı arayüzü | ✅ **Gerçekten çalışır** | Aynı |
| İkiz tür kartları | ✅ Tablodan gelir | Aynı |
| Acil durum ekranı | ✅ Statik içerik | Resmî kaynaklarla doğrulanmış |

**Demo veri setinin amacı:** "Sistem şu durumlarda şöyle davranır" göstermek. Model doğruluğu iddia etmiyoruz.

### Sunumda söylenecek cümle
> "Bu prototipte model çıktıları senaryo olarak elle verildi. Amacımız, gerçek bir model geldiğinde sistemin **tehlikeli durumlarda nasıl davranacağını** göstermek. Gerçek ürün için veri stratejimiz bu slaytta."

---

## 3. Demo veri seti

### 3.1 `species_info.csv` (20 tür)

Sütunlar: `id, latin_name, turkce_ad, risk, zehir_notu, belirti_baslangici, habitat, substrat, mevsim, ikiz_turler, ayirt_edici_ipucu, dogrulama_durumu, kaynak`

Risk dağılımı:

| Risk | Türler |
|---|---|
| `olumcul` | *Amanita phalloides*, *Galerina marginata*, *Cortinarius orellanus* |
| `yuksek` | *Amanita muscaria*, *A. pantherina*, *Gyromitra esculenta*, *Omphalotus olearius*, *Clitocybe rivulosa*, *Entoloma sinuatum* |
| `orta` | *Amanita rubescens*, *Agaricus xanthodermus*, *Morchella esculenta* (çiğ yenmemeli) |
| `dusuk` | *Agaricus campestris*, *Boletus edulis*, *Cantharellus cibarius*, *Lactarius deliciosus*, *Macrolepiota procera*, *Marasmius oreades*, *Pleurotus ostreatus*, *Coprinus comatus* |

> ⚠️ **Dürüst not:** Bu tabloyu genel mikoloji bilgisiyle hazırladım. Hepsi `dogrulama_durumu = TASLAK` ve `kaynak = DOĞRULANACAK` olarak işaretli. **Sunumdan önce her satırı en az bir akademik/resmî kaynakla doğrulayın** (Sağlık Bakanlığı / Zehir Danışma Merkezi yayınları, üniversite mikoloji makaleleri, GBIF Türkiye kayıtları). Türkçe adlar yöreden yöreye değişir; özellikle onları kontrol edin. `dusuk` etiketi "güvenli" demek değildir.

### 3.2 `demo_cases.json` (8 senaryo)

| # | Senaryo | Beklenen seviye | Neyi gösteriyor |
|---|---|---|---|
| c1 | Çayır mantarı + ölümcül ikiz *Amanita phalloides* | 🔴 | Birinci tahmin zararsız görünse de ikiz uyarısı |
| c2 | *A. phalloides* %91 | 🔴 | Ölümcül tür net + gecikmeli belirti uyarısı |
| c3 | Horoz mantarı + *Omphalotus* | 🔴 | Güven eşiği geçilse bile ikiz uyarısı |
| c4 | Kuzugöbeği + *Gyromitra* | 🔴 | "Kesilince içi boş mu?" ayırt edici soru |
| c5 | Bulanık fotoğraf | 🟡 | "Emin değilim" + yeni fotoğraf isteme |
| c6 | Taş/kozalak fotoğrafı | ⛔ | Mantar olmayan girdiyi reddetme |
| c7 | *Marasmius oreades* + *Clitocybe rivulosa* | 🔴 | Aynı çayırda gerçekçi karışıklık |
| c8 | *Pleurotus ostreatus* %88 | ⚪ | "Güvenli" demeden düşük riskli aday gösterme |

### 3.3 Karar katmanı (demo ile birebir uyumlu, bağımlılıksız)

```python
import json, csv

cfg = json.load(open("demo_cases.json", encoding="utf-8"))
T = cfg["esikler"]
info = {r["latin_name"]: r for r in csv.DictReader(open("species_info.csv", encoding="utf-8"))}

def decide(case):
    if case["mantar_olma_olasiligi"] < T["mantar_degil_esigi"]:
        return "MANTAR_DEGIL"
    top5 = case["simule_top5"]
    tehlikeli = [x for x in top5
                 if x["p"] >= T["tehlikeli_aday_min_olasilik"]
                 and info[x["latin_name"]]["risk"] in T["tehlikeli_risk_seviyeleri"]]
    if tehlikeli:
        return "KIRMIZI"
    top1 = top5[0]
    if top1["p"] < T["belirsizlik_esigi"] or info[top1["latin_name"]]["risk"] == "orta":
        return "SARI"
    return "GRI"

for c in cfg["senaryolar"]:
    sonuc = decide(c)
    print(c["id"], sonuc, "OK" if sonuc == c["beklenen_seviye"] else "HATA")
```

Bu betik 8 senaryonun hepsini `OK` verecek şekilde yazıldı; çalıştırıp doğrulayın (bu da README'ye girecek ilk "test" olabilir).

---

## 4. Gerçek ürün için sağlam veri stratejisi

Konsept prototipte model yok, ama jüri "gerçekte nasıl yapacaksınız?" diye soracak. Cevabımız 4 katmanlı bir veri planı:

### Katman 1 — Görüntü verisi (model eğitimi)

| Kaynak | İçerik | Rolü | Dikkat |
|---|---|---|---|
| **FungiTastic** (Kaggle: `picekl/fungitastic`) | ~350 bin gözlem, ~6 bin tür; fotoğraf + metadata (konum, habitat, substrat) + uydu/meteoroloji + maskeler; test setinin bir kısmı DNA doğrulamalı | **Ana kaynak** | "Mini" alt kümesi (215 sınıf) ile başla |
| **Danish Fungi 2020** | 1.604 tür, ~248 bin eğitim görüntüsü, uzmanlarca doğrulanmış etiketler | İkinci ana kaynak | Tam sürüm yüzlerce GB; mini veya 300px sürümü kullan |
| **iNaturalist** (araştırma-düzeyi gözlemler) | Dünya çapı, topluluk doğrulamalı | **Türkiye gözlemleri** | Yalnızca uygun lisanslı (CC) görüntüler |
| **GBIF** | Tür görülme kayıtları | Türkiye tür listesi, habitat/mevsim istatistiği | Medya lisanslarını tek tek kontrol et |
| **Kaggle `thehir0/mushroom-species`** | 100 tür, 50 binden fazla fotoğraf, Rusya'da çekilmiş | **Yardımcı**: hızlı baseline, ek veri | Lisans, sınıf listesi ve etiket kalitesi **doğrulanmadı**; yinelenen görüntü kontrolü şart |

### Katman 2 — Bilgi tabanı (risk ve ekoloji)
`species_info.csv` bu katmanın prototipidir. Gerçek üründe: uzman onaylı, her satırı kaynaklı, sürüm numaralı. **Zehirlilik bilgisi asla modelden çıkarılmaz; bilgi tabanından gelir.**

### Katman 3 — Türkiye saha verisi
- Üniversite mikoloji bölümleri ve doğa dernekleriyle iş birliği (doğrulanmış yerel fotoğraflar).
- Vaka istatistikleri için resmî kurumlarla iş birliği (**yalnızca anonim, toplu veri**).
- Hedef: Türkiye'de zehirlenme yapan türler için yerel fotoğraf kümesi.

### Katman 4 — "Altın test seti"
Eğitime **hiç girmeyen**, uzman veya DNA doğrulamalı, Türkiye'den bir test seti. Gerçek başarı sadece bunun üzerinde ölçülür.

### Veri kalite kontrol listesi
- [ ] Görüntü hash'iyle yinelenenleri temizle (train/test sızıntısını önle)
- [ ] Bölmeyi **gözlem kimliğine göre** yap (aynı mantarın fotoğrafları aynı tarafta)
- [ ] Her kaynağın lisansını `docs/veri-kaynaklari.md`'ye yaz
- [ ] Etiket kalitesi için rastgele 100 görüntüyü elle kontrol et
- [ ] "Mantar değil" sınıfı için negatif örnekler (taş, kozalak, çiçek, ağaç kabuğu) topla
- [ ] Ayrı bir "bilinmeyen tür" test kümesi hazırla

> ⚠️ **Lisans uyarısı:** Danimarka mikoloji verisiyle ilişkili bazı kaynaklarda CC BY-NC 4.0 (ticari olmayan) lisansı belirtiliyor. Hackathon/araştırma için sorun değil, **ticari ürün düşünürseniz lisansları tek tek kontrol edin.**

---

## 5. Mimari

```
Kullanıcı fotoğrafı
      │
      ▼
[1] Mantar mı? kapısı ──hayır──► ⛔ "Mantar fotoğrafı yükle"
      │evet
      ▼
[2] Görüntü modeli ──► Top-5 tür + olasılık        ← PROTOTİPTE SİMÜLE
      │
      ▼
[3] Karar katmanı (kural tabanlı)                   ← GERÇEK ÇALIŞIR
    • tehlikeli aday var mı?  → 🔴
    • güven < %60 / şartlı tür → 🟡
    • aksi halde             → ⚪ (uzman onayı uyarısıyla)
      │
      ▼
[4] species_info.csv ile eşleştir                   ← GERÇEK ÇALIŞIR
    habitat, mevsim, ikiz türler, ayırt edici ipucu
      │
      ▼
Sonuç ekranı + sabit uyarı bandı + acil durum butonu
```

**Prototip arayüzü (önerim):** Tek bir `index.html`, ek kütüphane yok. `species_info.csv` ve `demo_cases.json` dosyalarını okuyup 8 senaryoyu butonlarla gösterir. CSV'yi 15 satırlık saf JS ile ayrıştırabilirsiniz. İnternetsiz de çalışır.

---

## 6. Yol haritası: prototipten ürüne

| Aşama | Ne yapılır | Çıktı |
|---|---|---|
| **A. Konsept prototip (hackathon)** | Simüle senaryolar + gerçek karar katmanı + arayüz | Çalışan demo, açık GitHub reposu |
| **B. Mini kanıt (opsiyonel, 1-2 saat)** | Colab'da 10 türlük küçük bir model (transfer öğrenme) → gerçek top-5 çıktısını karar katmanına bağla | "İlk gerçek sonuç" slaytı |
| **C. Pilot** | Türkiye için 30-50 tür, FungiTastic + iNaturalist + yerel saha verisi, uzman doğrulaması | Ölçülmüş sonuçlar, altın test seti |
| **D. Ürün** | Çevrimdışı mobil uygulama, risk haritası, uzman geri bildirim kuyruğu | Güvenlik denetiminden geçmiş sürüm |

**B aşaması için kısa örnek (isteğe bağlı):**

```python
import torch, torchvision.models as models, torch.nn as nn
model = models.mobilenet_v3_large(weights="IMAGENET1K_V2")
model.classifier[-1] = nn.Linear(model.classifier[-1].in_features, 10)  # 10 tür
# önce sadece son katman, sonra düşük öğrenme oranıyla tümü
```

**Gerçek ürün aşamasında ölçülecek hedef metrikler** (prototipte iddia edilmez):

| Metrik | Neden |
|---|---|
| **Zehirli tür recall'u** | Ana güvenlik metriği |
| **Tehlikeli karışıklık oranı** (zehirliyi "düşük riskli" gösterme) | Sıfıra yakın olmalı |
| Top-5 doğruluk | Genel başarı |
| Kalibrasyon (ECE) | "%90 eminim" gerçekten %90 mı? |
| Reddetme eğrisi | Eşik yükselince doğruluk/ret dengesi |

---

## 7. Özellik listesi

### Prototipte gösterilecekler (öncelik sırasıyla)
1. Fotoğraf yükleme/seçme ekranı (senaryo butonlarıyla)
2. Top-5 aday + olasılık çubukları
3. 🔴🟡⚪⛔ seviye göstergesi + sabit uyarı bandı
4. **İkiz tür kartı** ("Bunu sakın karıştırma")
5. Tür bilgi kartı: habitat, substrat, mevsim, ayırt edici ipucu
6. "Emin değilim" ekranı + **"sap tabanını da çek"** yönlendirmesi
7. **Acil durum ekranı:** "Yedim, ne yapmalıyım?" (Ulusal Zehir Danışma Merkezi **114**, **112**, belirtiler gecikmeli başlayabilir, mantardan örnek sakla). *Numaraları sunumdan önce resmî kaynaktan doğrulayın.*

### Gelecek vizyonu slaytı için
- Metadata ile iyileştirme (konum + ay + habitat), aralık ayında çıkmayan tür tahminini eler
- Çok fotoğraflı gözlem (üst/alt/sap tabanı)
- Grad-CAM ile "model nereye baktı?" açıklaması
- Çevrimdışı mod (ONNX + tarayıcı)
- Bölgesel anonim risk haritası ve mevsimsel uyarı bildirimi
- Quiz / eğitim modu (okullar için)
- Uzman doğrulama kuyruğu
- Spor baskı rehberi
- Sesli sonuç okuma (yaşlılar ve görme güçlüğü için)

### Bilerek yapmadıklarımız
- Pişirme/yeme önerisi
- "Güvenli" etiketi
- Tek fotoğrafa tam güven

---

## 8. GitHub planı (yarışma şartı: açık repo, adım adım güncel)

```
mycoguard/
├── README.md
├── LICENSE
├── docs/
│   ├── proje-plani.md
│   ├── veri-kaynaklari.md     # her kaynağın linki, lisansı, tarihi
│   ├── guvenlik-etik.md
│   └── gunluk.md              # her gün 3-5 satır
├── data/
│   ├── species_info.csv       # küçük, repoya girer
│   ├── demo_cases.json
│   └── README.md              # gerçek veri nasıl indirilir (veri repoya konmaz)
├── src/
│   └── decide.py              # karar katmanı + test
├── app/
│   └── index.html             # prototip arayüz
└── results/
```

**Commit mesajı örnekleri:**
```
data: species_info.csv ilk 20 tür eklendi
core: karar katmanı ve 8 demo senaryosu testi
app: sonuç ekranı ve uyarı bandı
docs: veri stratejisi (4 katman) yazıldı
docs: günlüğe 1. gün notları
```

**README'ye girecekler:** problem + çözüm, demo GIF'i, nasıl çalıştırılır, **"neyin simüle olduğu"** tablosu, veri stratejisi, sınırlılıklar ve sorumluluk reddi, takım ve görev dağılımı.

---

## 9. Takım görev dağılımı

| Rol | Sorumluluk |
|---|---|
| **Küratör** | `species_info.csv` doğrulama, kaynak linkleri, ikiz türler |
| **Arayüz** | `index.html`, seviye ekranları, acil durum ekranı |
| **Karar katmanı ve test** | `decide.py`, senaryo testleri, (opsiyonel) Colab mini model |
| **Sunum ve GitHub** | README, günlük, demo videosu, slaytlar |

---

## 10. Zaman planı (oransal)

| Faz | Oran | Çıktı |
|---|---|---|
| Hazırlık | ~15% | Repo, dosyalar yüklendi, görev dağılımı |
| Veri doğrulama | ~25% | `species_info.csv` kaynaklarla doğrulandı |
| Arayüz + karar katmanı | ~30% | 8 senaryo uçtan uca çalışıyor |
| (Opsiyonel) Mini model | ~10% | 10 türlük gerçek bir sonuç |
| Sunum | ~20% | Slaytlar, demo videosu, prova |

**Altın kural:** Erken bir çalışan demo, geç bir mükemmel demodan iyidir. Yedek olarak ekran kaydı hazır olsun.

---

## 11. Sunum akışı (5-7 dk)

1. **Açılış (30 sn):** Güncel zehirlenme haberi/istatistiği (kaynaklı)
2. **Problem (30 sn):** Fotoğraftan tanıma neden zor ve neden ölümcül
3. **Fikir (1 dk):** MycoGuard "yenilebilir" demez, **risk uyarır**
4. **Canlı demo (2 dk):** c1 (ikiz uyarısı) → c3 (güven yüksek ama yine uyarı) → c5 ("emin değilim") → c8 ("güvenli" demiyor)
5. **Dürüst ayrım (30 sn):** "Model çıktıları simüle, karar katmanı gerçek"
6. **Gerçek ürün için veri stratejisi (1 dk):** 4 katman, altın test seti, uzman iş birliği
7. **Etki ve yol haritası (30 sn):** A → B → C → D

**Beklenen jüri soruları:**
- *"Model yanlış yaparsa?"* → En kötü aday kuralı, belirsizlik eşiği, asimetrik maliyet, sorumluluk reddi
- *"Verileriniz nereden?"* → Bölüm 4
- *"Bu bir doktor/uzman yerine geçer mi?"* → Hayır; uygulama uzman onayını teşvik eder
- *"Neden gerçek model yok?"* → Önce güvenlik davranışını kanıtladık; sağlam veri olmadan ürün iddiası etik olmaz

---

## 12. Riskler

| Risk | Önlem |
|---|---|
| `species_info.csv` yanlış bilgi içerir | Tüm satırlar kaynakla doğrulanmadan sunuma çıkma |
| Demo, gerçek model sanılır | Her ekranda "SİMÜLE DEMO" rozeti + sunumda açık beyan |
| Kullanıcı sonucu onay sanır | Yeşil renk yok, "güvenli" kelimesi yok |
| Lisans sorunu (gerçek veri aşamasında) | `veri-kaynaklari.md` ile takip |
| Hukuki sorumluluk | Sorumluluk reddi + uzman onayı + acil durum numarası |

---

## 13. Bugünkü checklist

- [ ] Public GitHub reposu aç, 3 dosyayı yükle
- [ ] `decide.py` olarak karar betiğini çalıştır, 8 senaryo OK mu?
- [ ] `species_info.csv` doğrulamayı böl (her kişi 5 tür)
- [ ] Kaggle'dan FungiTastic-Mini ve `thehir0/mushroom-species` sayfalarını incele, lisansları `veri-kaynaklari.md`'ye yaz
- [ ] Arayüz taslağı için `index.html` iskeletini başlat
- [ ] `docs/gunluk.md` ilk girişi yaz

---

## 14. Kaynaklar (doğruladıklarım)

- FungiTastic (CVPRW 2025): `bohemianvra.github.io/FungiTastic`, Kaggle `picekl/fungitastic`, arXiv 2408.13632
- Danish Fungi 2020 (WACV 2022): arXiv 2103.10107, `sites.google.com/view/danish-fungi-dataset`
- FungiCLEF 2023: `imageclef.org/FungiCLEF2023`
- UCI Mushroom: `kaggle.com/datasets/uciml/mushroom-classification` (tablo tabanlı, 1981 rehberinden hipotetik örnekler; gerçek dünya başarısı göstermez)
- Kaggle Mushroom species: `kaggle.com/datasets/thehir0/mushroom-species` (yalnızca kısa açıklama doğrulandı)

> **Sunumdan önce mutlaka doğrulanacaklar:** `species_info.csv`'deki tüm satırlar, acil durum numaraları, tüm veri setlerinin güncel lisansları.
