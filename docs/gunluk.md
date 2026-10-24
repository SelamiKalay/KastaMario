# Proje günlüğü

## 24 Ekim 2026 — 1. gün (sabah)
- Proje planı yazıldı; repo yapısı kuruldu.
- `species_info.csv` (20 tür) ve `demo_cases.json` (8 örnek vaka) eklendi.
- Karar katmanı `src/decide.py`: 8/8 vaka OK.
- İlk arayüz: vaka butonları, top-5 çubukları, seviye ekranı, ikiz tür kartları, acil durum ekranı.

## 24 Ekim 2026 — 1. gün (öğleden sonra)
- Kapsam Kastamonu'ya odaklandı; bilgi tabanı 28 türe çıktı (Ak köygöçüren, Lepiota, Kükürt mantarı, Şeytan mantarı, Bal mantarı, Yumurta mantarı, Kirpi, Borazan…). Yeni alanlar: belirtiler, belirti saatleri, ilk yardım, boy, yetişme süreci, aylar, toplama notu, Kastamonu notu.
- Yarışma kuralları (MLH Open Source AI) incelendi → açık ağırlıklı model olarak **Gemma 4** seçildi (önce yerel E4B planlandı, sonra uzak API'ye geçildi).
- Gemma 4 sunucusu (`server/`): yapılandırılmış görsel özellik çıkarımı + yalnızca riski yükselten kurallar + bilgi tabanına dayalı asistan.
- Veri hattı: `ml/collect.py` (iNaturalist + GBIF), `ml/clean.py` (10 adımlı temizlik, dHash kopya tespiti, sızıntısız ayrım), `ml/train.py` (EfficientNet-B0, kalibrasyon, güvenlik metrikleri, ONNX).
- Arayüz yeniden tasarlandı: Kastamonu teması, 5 sekme (Tara, Rehber, Asistan, Takvim, Yedim!), karanlık mod, PWA.
- Testler: 141 test geçti (karar katmanı, tür tablosu, Python↔JS eşdeğerliği, Gemma kuralları, temizlik fonksiyonları).
- Not: Windows Smart App Control pandas DLL'ini engelledi → veri hattı csv + numpy ile yazıldı.

## 24 Ekim 2026 — 1. gün (akşam)
- Asistan uzak API'ye taşındı: Gemini API üzerinden Gemma 4 (`gemma-4-26b-a4b-it`, ücretsiz katman); OpenAI uyumlu sağlayıcılar yedek. CORS ve IP başına istek sınırı eklendi.
- Mobil yol belirlendi: tür tahmini, rehber, takvim ve acil durum telefonda internetsiz; Gemma adımları sunucu üzerinden. DigitalOcean App Platform tanımı ve Capacitor yapılandırması eklendi (`docs/mobil.md`).
- Arayüz Anthropic frontend-design yönergeleriyle yeniden tasarlandı: mantar anatomisi çizimi ana öğe, Gemma bulguları çizim üzerinde işaretleniyor; fenoloji tablosu; tehlike etiketi biçiminde sonuç.
- GBIF verisiyle Karadeniz'de kaydı olmayan 3 tür rehberden çıkarıldı (25 tür kaldı).
- Not: PyTorch'un CUDA 12.8 deposunda Python 3.14 için torch+torchvision eşleşmesi yok; CUDA 13.0 deposuna geçildi.

## 24 Ekim 2026 — 1. gün (gece)
- Gemma 4 "düşünme" seviyesi minimal yapıldı: iki fotoğraflı analiz ~180 sn → ~5 sn, bulgular aynı.
- Asistana 25 türün tam kataloğu verildi; yanıtlar madde madde ve biçimli. Üç açılı fotoğraf ve paralel analiz eklendi.
- Rehber 25 türün tamamı için CC lisanslı fotoğraf ve kaynaklarla (iNaturalist, GBIF, iki hakemli klinik derleme) yenilendi; anatomi gerçek bir köygöçüren fotoğrafı (CC0) üzerinde.
- Takvim ay seçici + seçili ay görünümü + tüm yıl tablosu olarak yeniden tasarlandı; yazı tipleri çevrimdışı kullanım için uygulamaya gömüldü; 114 (UZEM) resmî kaynakla doğrulandı.
- Veri: 15.013 ham fotoğraftan temizlikle 11.167 fotoğraf, 26 sınıf, sızıntısız ayrım.
- Eğitim ilk denemede çok yavaştı (Windows DataLoader, ~9,5 sn/adım; GPU tek başına 0,26 sn/adım). Fotoğraflar GPU belleğinde tutulup veri artırma GPU'ya taşındı. Eğitim, bilgisayar soğuduktan sonra yapılacak.
