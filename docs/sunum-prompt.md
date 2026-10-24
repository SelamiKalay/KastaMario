# Sunum promptu (Gamma, Canva Magic Design, Google Slides, PowerPoint Copilot vb. için)

Aşağıdaki metnin tamamını kopyalayıp sunum aracına yapıştırın. Kullanılacak görseller:
- ekran görüntüleri: `docs/img/`
- logo: `app/img/kastamario.png`
- asistan: `app/img/mybear.png`

---

**Görev:** "KastaMario" adlı yapay zekâ destekli mantar zehirlenme risk uygulaması için **tam 6 slaytlık**, Türkçe, 16:9 bir hackathon sunumu hazırla.

**Bağlam:** Hackathon'un konusu yapay zekâlı bir uygulama geliştirmek (MLH "Best Open-Source AI Project"). Toplam süre 7–8 dakika: slaytlar yaklaşık 4 dakika, canlı telefon demosu 3–4 dakika.

**Odak:** Yazılım ve teknik ayrıntıdan çok ana fikir ve uygulamanın ne kadar işe yaradığı. Teknik terim (EfficientNet, ONNX, RAG, JSON) kullanma. Yapay zekâya tek bir slayt ayır, onu da sade anlat.

**Görsel stil:**
- Renkler:
  - çok koyu orman yeşili zemin (#0d2113), krem metin (#f8f0e0);
  - ikinci zemin krem (#f4ecdc) üzerinde koyu yeşil metin;
  - vurgu altın sarısı (#f3c75c);
  - tehlike vurgusu mercan kırmızısı (#ff8f84, açık zeminde #a3261b).
- Yazı tipleri: başlıklar zarif serif (Newsreader), gövde metni sade sans-serif (IBM Plex Sans).
- Her slaytta tek fikir: büyük sayılar, ekran görüntüleri, kısa cümleler.
- Yeşil renk "güvenli" anlamında asla kullanılmasın. Clip-art yok.

**Slaytlar:**

1. **Kapak** (20 sn)
   - Başlık: "KastaMario".
   - Alt başlık: "Yapay zekâ ile mantar zehirlenmelerinin önüne geçmek".
   - Küçük üst etiket: "MLH · Best Open-Source AI Project".
   - Sağda logo (mantar şapkalı ayı).

2. **Sorun: bu ayın haberleri** (1 dk)
   - Büyük sayı: "40+". Altında: "kişi Kastamonu'da bir haftada mantardan zehirlenerek hastaneye başvurdu (5 Ekim 2026)".
   - Yanında üç haber kartı:
     - Cide, Kastamonu, 4 Ekim: 3'ü çocuk 5 kişi hastanelik, 3'ü Ankara'ya sevk.
     - Sinop, 1 Eylül–14 Ekim: 76 başvuru; geçen yıl aynı dönemde 1 ölüm.
     - Yahyalı, Kayseri, 19 Ekim: 12 kişi hastaneye kaldırıldı.
   - Konuşmada: zehirli mantarı evde ayırt etmenin yolu yok; kanlıca toplanırken ölümcül köygöçüren karışabiliyor; belirtiler 6–24 saat gecikiyor.
   - Kaynak satırı: sondakika.com, Yeniçağ, Taşköprü Postası, Kayseri İlk Haber.

3. **Çözüm: KastaMario ne işe yarıyor?** (1 dk)
   - Başlık: "Mantarın fotoğrafını çek, riskini ve ne yapman gerektiğini öğren".
   - Dört telefon ekran görüntüsü yan yana, her birinin altında kullanım anı:
     - Toplamadan önce: zehirli olabilir mi, ölümcül ikizi hangisi?
     - Tanımak için: 27 yöre türü (saçak ve koçak dahil), belirti, ilk yardım, yetiştiği yer.
     - Mevsiminde: bu ay hangi ölümcül türler çıkıyor?
     - Yedikten sonra: tek dokunuşla 114 / 112, geç belirti uyarısı.
   - Alt satır: "Telefona uygulama olarak eklenir · ormanda internet yokken de çalışır · hiçbir mantara 'yenilebilir' demez".

4. **Yapay zekâ: uygulamanın kalbi** (1,5 dk, hackathon konusu)
   - Başlık: "Fotoğrafa iki yapay zekâ bakıyor, şüphe varsa uyarıyor".
   - Basit akış:
     - [Görüntü modeli: 12.000+ fotoğrafla kendimiz eğittik, telefonda internetsiz 27 türü tanır]
     - [Gemma 4, Google'ın açık modeli: torba, halka gibi ölümcül işaretleri arar; Mybear asistanı olarak soruları yanıtlar]
     - → [Güvenlik kuralı: adaylardan biri bile ölümcül olabilirse sonuç KIRMIZI; yapay zekâ riski yükseltebilir, asla düşüremez].
   - Altta üç büyük sayı:
     - %99,3: ölümcül tür fotoğrafı KIRMIZI gösterildi.
     - 0,14 sn: telefonda sonuç süresi.
     - %98,6: doğru tür ilk 5 tahminde.

5. **Canlı demo** (3–4 dk)
   - Başlık: "Uygulamayı birlikte deneyelim". Numaralı 5 adım ve sağda Mybear görseli:
     1. Köygöçüren fotoğrafı → KIRMIZI.
     2. Kanlıca fotoğrafı → olası türler ve ölümcül ikizi.
     3. Mybear'a "Güvenmediğim bir mantar yedim, ne yapmalıyım?".
     4. Takvimde Ekim'in ölümcül türleri.
     5. Yedim! ekranında belirti 8 saat sonra → ölümcül uyarısı.

6. **Kapanış** (30 sn)
   - "Teşekkürler".
   - "Bu sonbahar bir sepet mantar, bir hastane yatağına dönüşmesin."
   - Üç etiket: Açık kaynak · MIT / Gemma 4 açık model / İnternetsiz çalışır.
   - GitHub: github.com/SelamiKalay/BAKLAVA.
   - "Acil durumda: 114 Ulusal Zehir Danışma Merkezi · 112".

**Konuşmacı notları:** Her slayta, süresine uygun, sade ve samimi Türkçe bir konuşmacı notu ekle. Yapay zekânın katkısını somut örnekle anlat (ör. "fotoğrafta torba görürse sonucu kırmızıya çeker").

**Kaçınılacaklar:** "taslak", "prototip", "simülasyon" kelimeleri; uydurma istatistik; "yenilebilir/güvenli" ifadesi; teknik jargon; 6'dan fazla slayt.
