# Sunum promptu (Gamma, Canva Magic Design, Google Slides, PowerPoint Copilot vb. için)

Aşağıdaki metnin tamamını kopyalayıp sunum aracına yapıştırın. Ekran görüntüleri `docs/img/` klasöründe, logo `app/img/kastamario.png`, asistan görseli `app/img/mybear.png`, anatomi fotoğrafı `app/img/anatomi.jpg`.

---

**Görev:** "KastaMario" adlı açık kaynak, yapay zekâ destekli mobil mantar zehirlenme risk uygulaması için 13 slaytlık, Türkçe, 16:9 bir hackathon sunumu hazırla. Sunum MLH Hacktoberfest Hack Day "Best Open-Source AI Project" jürisine 5–7 dakikada yapılacak. Ardından uygulama telefondan canlı gösterilecek.

**Ana mesaj:** Kastamonu'da her sonbahar yaşanan mantar zehirlenmelerinin önüne geçmek için, açık ağırlıklı Gemma 4 ve kendi eğittiğimiz görüntü modelini bir güvenlik katmanıyla birleştirdik. Yapay zekânın ne yaptığı sunumun merkezinde olmalı.

**Görsel stil:**
- Çok koyu orman yeşili zemin (#0d2113), krem metin (#f8f0e0), ikinci zemin olarak krem (#f4ecdc) ve üzerinde koyu yeşil metin.
- Vurgu renkleri: altın sarısı (#f3c75c), tehlike için mercan kırmızısı (#ff8f84, açık zeminde #a3261b).
- Başlıklar zarif serif (Newsreader veya benzeri), gövde metni temiz sans-serif (IBM Plex Sans).
- Her slaytta tek fikir; madde listesi yerine kartlar, büyük sayılar, ekran görüntüleri kullan. Yeşil renk "güvenli" anlamında asla kullanılmasın.
- Doğa ve orman hissi olsun ama ciddi ve profesyonel kalsın. Clip-art kullanma.

**Slaytlar:**

1. **Kapak.** Başlık "KastaMario", alt başlık "Yapay zekâ ile mantar zehirlenmelerinin önüne geçmek". Küçük üst etiket: "MLH · Best Open-Source AI Project". Sağda KastaMario logosu (mantar şapkalı ayı).

2. **Sorun: güncel haberler (Ekim 2026).** Büyük sayı: "40+". Altında: "kişi Kastamonu'da bir haftada mantardan zehirlenerek hastaneye başvurdu (5 Ekim 2026)". Yanında üç küçük haber kartı:
   - Cide, Kastamonu, 4 Ekim: 3'ü çocuk 5 kişi hastanelik oldu, 3'ü Ankara'ya sevk edildi.
   - Sinop, 1 Eylül–14 Ekim: 76 kişi başvurdu (Sinop Valiliği verisi); geçen yıl aynı dönemde 1 kişi hayatını kaybetti.
   - Yahyalı, Kayseri, 19 Ekim: toplanan mantarı yiyen 12 kişi hastaneye kaldırıldı.
   Alt satırda kaynaklar: sondakika.com, Yeniçağ, Taşköprü Postası, Kayseri İlk Haber.

3. **Neden oluyor?** Başlık "Zehirli mantarı evde ayırt etmenin bir yolu yok". Üç kart:
   - Benzer görünüyorlar: yöre halkı kanlıca toplar; ölümcül köygöçüren sepete karışabilir.
   - Belirtiler gecikiyor: ölümcül türlerde 6–24 saat sonra başlar, karaciğer hasarı ilerler.
   - Halk testleri yanlış: gümüş kaşık, sirke, soğanla pişirme geçersiz.
   Kaynak: Doç. Dr. Çiğdem Sevim, Kastamonu Üniversitesi Tıp Fakültesi.

4. **Çözüm: KastaMario.** Dört telefon ekran görüntüsü yan yana, altlarında kısa etiketler:
   - Tara: 3 açıdan fotoğraf, risk ve olası türler.
   - Rehber: 27 Kastamonu türü, yöresel saçak ve koçak dahil.
   - Takvim: hangi ay hangi mantar çıkar.
   - Yedim!: 114 / 112 ve belirti saati.

5. **Yapay zekâ hattı (diyagram).** Soldan sağa akış:
   - [1] EfficientNet-B0: cihazda, internetsiz; 27 tür + "mantar değil".
   - [2] Gemma 4 26B A4B: sunucuda, aynı anda; fotoğraftaki ayırt edici işaretleri JSON olarak çıkarır.
   - İkisi birleşip → [3] Güvenlik kuralları:
     - adaylardan biri ≥%5 tehlikeliyse KIRMIZI,
     - %60 altı güvende "emin değiliz",
     - Gemma riski yalnızca yükseltir.
   - → üç sonuç etiketi: KIRMIZI zehirli olabilir / SARI emin değiliz / GRİ düşük riskli aday.

6. **Gemma 4 ne yapıyor? (en önemli slayt).** Dört kart ve sağda anatomi fotoğrafı:
   - Görsel işaretler: torba, halka, lamel rengi, alt yüz, substrat; sabit şemalı JSON.
   - Risk yükseltme: torba görürse sonucu KIRMIZI'ya çeker; düşürmesi kuralla engelli.
   - Mybear asistan: 27 türlük bilgi tabanıyla (RAG) akışlı Türkçe yanıt, yasak ifade süzgeci.
   - 36× hızlandırma: düşünme seviyesi "minimal" ile iki fotoğraflı analiz ~180 sn → ~5 sn.
   Not: Gemma 4 açık ağırlıklı, Apache 2.0 lisanslı.

7. **Gemma 4'ün ölçülmüş katkısı (dürüst sonuç).** 151 test fotoğrafı iki yoldan geçirildi: yalnızca model ve model + Gemma 4. Üç büyük sayı:
   - "0": Gemma hatası.
   - "%0": düşük riskli türde gereksiz KIRMIZI alarm.
   - "%8": Amanita fotoğraflarında torbayı görme oranı (n=24).
   "Ne öğrendik?" kutusu: görüntü modeli tehlikeli türlerin %98,8'ini zaten yakaladığı için Gemma bu sette ek fotoğraf kurtarmadı. Torba çoğu fotoğrafta toprağın içinde kaldığı için uygulama ayrıca sap tabanı fotoğrafı istiyor. Gemma'nın asıl katkısı açıklanabilirlik, Mybear asistanı ve ikinci güvenlik ağı.

8. **Veri madenciliği.** Dört adımlı akış:
   - Toplama: iNaturalist + GBIF.
   - Temizleme: dHash yakın kopya silme, lisans süzgeci, taksonomi normalleştirme.
   - Ayrıştırma: gözlem gruplu bölme, dengeleme 60–450.
   - Temiz set: 8.462 eğitim / 1.816 doğrulama / 1.779 test, 28 sınıf.

9. **Sonuçlar (büyük sayılar).**
   - %98,6 doğru tür ilk 5 tahminde (top-1 %90,7).
   - %99,3 ölümcül tür fotoğrafı KIRMIZI.
   - %94,6 internetten bulunan 315 fotoğrafta doğru tür ilk 5'te.
   - 0,14 sn telefonda tahmin.
   Not: dış testte iyileştirme top-1 %75,6 → %78,4, top-5 %91,4 → %94,6.

10. **Güvenlik tasarımı (kırmızı zeminli vurgu slaytı).** Büyük cümle: "KastaMario hiçbir mantara 'yenilebilir' demez." Alt metin: zehirliyi yenilebilir sanmak ölümcül olabilir; yenilebiliri zehirli sanmanın bedeli boş bir sepettir. Dört etiket:
    - En kötü aday kuralı
    - Gemma yalnızca yükseltir
    - Yasak ifade süzgeci
    - Yeşil risk rengi yok

11. **Neden bu etkinliğe uygun?** Üç kart:
    - Tamamen açık: MIT kod, açık veri, katkı rehberi, 166 otomatik test.
    - Açık ağırlıklı yapay zekâ: Gemma 4 kararın parçası.
    - Gerçek kullanıcı: Kastamonu'daki mantar toplayan aileler, ormanda internetsiz çalışır.
    Alt satır: github.com/SelamiKalay/BAKLAVA

12. **Canlı demo planı.** Numaralı 5 adım ve Mybear görseli:
    1. Köygöçüren fotoğrafı → KIRMIZI.
    2. Kanlıca fotoğrafı → olası türler ve ölümcül ikizi.
    3. Mybear'a "Güvenmediğim bir mantar yedim, ne yapmalıyım?" sorusu.
    4. Takvimde Ekim'in ölümcül türleri.
    5. Yedim! ekranında belirti 8 saat sonra → ölümcül uyarısı.

13. **Kapanış.** "Teşekkürler" ve "Bu sonbahar bir sepet mantar, bir hastane yatağına dönüşmesin." GitHub adresi ve "Acil durumda: 114 Ulusal Zehir Danışma Merkezi · 112".

**Konuşmacı notları:** Her slayta 3–5 cümlelik, sade ve samimi bir Türkçe konuşmacı notu ekle. Toplam konuşma 5–7 dakikayı geçmesin. Gemma 4'ün ve yapay zekânın katkısını her fırsatta somut örnekle anlat (ör. "görüntü modeli çayır mantarı derken Gemma sap tabanında torba gördü ve sonucu kırmızıya çekti").

**Kaçınılacaklar:** "taslak", "prototip", "simülasyon" kelimeleri; uydurma istatistik; "yenilebilir/güvenli" ifadesi; yeşil renkle güvenlik vurgusu.
