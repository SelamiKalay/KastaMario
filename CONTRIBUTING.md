# Katkı rehberi

KastaMario açık kaynaklıdır (MIT). Katkılar memnuniyetle karşılanır; Hacktoberfest katkıları dahil.

## Nasıl katkı verilir?
1. Depoyu çatallayın (fork), yeni bir dal açın: `git checkout -b ozellik/kisa-ad`
2. Değişikliği yapın, testleri çalıştırın: `python -m pytest -q` (hepsi geçmeli)
3. Uygulamadaki JS/CSS dosyalarını değiştirdiyseniz `python src/build_app_data.py` ile sürüm etiketlerini yenileyin.
4. Açıklayıcı bir mesajla birleştirme isteği (pull request) açın.

## Katkı fikirleri
- **Yeni tür:** `data/species_info.csv` dosyasına Kastamonu'da kayıtlı bir tür ekleyin (kaynak bağlantısıyla), sonra `ml/collect.py → clean.py → train.py` hattıyla modeli yeniden eğitin.
- **Fotoğraf:** iNaturalist'e Kastamonu'dan mantar gözlemi yükleyin; sonraki eğitimde veri setine girer.
- **Dil:** arayüz metinlerini İngilizceye çevirme.
- **Doğruluk:** tür bilgilerinde (belirti süresi, yetişme zamanı, ilk yardım) hata görürseniz kaynakla birlikte bildirin.

## Kırmızı çizgiler (güvenlik)
- Uygulama hiçbir mantar için "yenilebilir" ya da "güvenli" demez. Bu kuralı gevşeten değişiklik kabul edilmez.
- Gemma ya da başka bir model riski **yalnızca yükseltebilir**, düşüremez (`app/decide.js` ve `src/decide.py` aynı kalmalı; `tests/test_parity.py` bunu denetler).
- API anahtarları depoya girmez; `.env` dosyası `.gitignore` içindedir.
