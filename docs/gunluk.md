# Proje günlüğü

## 24 Ekim 2026 — 1. gün (sabah)
- Proje planı yazıldı; repo yapısı kuruldu.
- `species_info.csv` (20 tür) ve `demo_cases.json` (8 örnek vaka) eklendi.
- Karar katmanı `src/decide.py`: 8/8 vaka OK.
- İlk arayüz: vaka butonları, top-5 çubukları, seviye ekranı, ikiz tür kartları, acil durum ekranı.

## 24 Ekim 2026 — 1. gün (öğleden sonra)
- Kapsam Kastamonu'ya odaklandı; bilgi tabanı 28 türe çıktı (Ak köygöçüren, Lepiota, Kükürt mantarı, Şeytan mantarı, Bal mantarı, Yumurta mantarı, Kirpi, Borazan…). Yeni alanlar: belirtiler, belirti saatleri, ilk yardım, boy, yetişme süreci, aylar, toplama notu, Kastamonu notu.
- Yarışma kuralları (MLH Open Source AI) incelendi → açık ağırlıklı model olarak **Gemma 4 E4B** seçildi.
- Gemma 4 sunucusu (`server/`): yapılandırılmış görsel özellik çıkarımı + yalnızca riski yükselten kurallar + bilgi tabanına dayalı asistan.
- Veri hattı: `ml/collect.py` (iNaturalist + GBIF), `ml/clean.py` (10 adımlı temizlik, dHash kopya tespiti, sızıntısız ayrım), `ml/train.py` (EfficientNet-B0, kalibrasyon, güvenlik metrikleri, ONNX).
- Arayüz yeniden tasarlandı: Kastamonu teması, 5 sekme (Tara, Rehber, Asistan, Takvim, Yedim!), karanlık mod, PWA.
- Testler: 141 test geçti (karar katmanı, tür tablosu, Python↔JS eşdeğerliği, Gemma kuralları, temizlik fonksiyonları).
- Not: Windows Smart App Control pandas DLL'ini engelledi → veri hattı csv + numpy ile yazıldı.
