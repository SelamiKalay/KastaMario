// OTOMATİK ÜRETİLDİ: python src/build_app_data.py — elle düzenlemeyin.
window.MYCO_CASES = {
 "aciklama": "MycoGuard konsept prototipi için 8 demo senaryosu. Model çıktıları SİMÜLEDİR (elle verilmiştir); gerçek bir modelden gelmez.",
 "surum": "0.1.0",
 "esikler": {
  "mantar_degil_esigi": 0.5,
  "tehlikeli_aday_min_olasilik": 0.05,
  "tehlikeli_risk_seviyeleri": [
   "olumcul",
   "yuksek"
  ],
  "belirsizlik_esigi": 0.6
 },
 "senaryolar": [
  {
   "id": "c1",
   "baslik": "Çayır mantarı + ölümcül ikiz",
   "aciklama": "Çayırda bulunan beyaz şapkalı mantar. Birinci tahmin zararsız görünüyor ama ölümcül Amanita phalloides adaylar arasında.",
   "foto_ipucu": "Beyaz şapka, çimenlik alan, sap tabanı görünmüyor",
   "mantar_olma_olasiligi": 0.97,
   "simule_top5": [
    {
     "latin_name": "Agaricus campestris",
     "p": 0.62
    },
    {
     "latin_name": "Amanita phalloides",
     "p": 0.18
    },
    {
     "latin_name": "Agaricus xanthodermus",
     "p": 0.1
    },
    {
     "latin_name": "Macrolepiota procera",
     "p": 0.06
    },
    {
     "latin_name": "Coprinus comatus",
     "p": 0.04
    }
   ],
   "beklenen_seviye": "KIRMIZI"
  },
  {
   "id": "c2",
   "baslik": "Köygöçüren (%91)",
   "aciklama": "Meşe altında yeşilimsi şapkalı mantar. Ölümcül tür net biçimde birinci aday.",
   "foto_ipucu": "Zeytin yeşili şapka, beyaz lameller, sapta halka",
   "mantar_olma_olasiligi": 0.99,
   "simule_top5": [
    {
     "latin_name": "Amanita phalloides",
     "p": 0.91
    },
    {
     "latin_name": "Amanita rubescens",
     "p": 0.04
    },
    {
     "latin_name": "Amanita pantherina",
     "p": 0.03
    },
    {
     "latin_name": "Agaricus campestris",
     "p": 0.01
    },
    {
     "latin_name": "Entoloma sinuatum",
     "p": 0.01
    }
   ],
   "beklenen_seviye": "KIRMIZI"
  },
  {
   "id": "c3",
   "baslik": "Horoz mantarı + zeytin mantarı",
   "aciklama": "Turuncu-sarı mantar. Birinci tahmin güven eşiğini geçiyor ama zehirli ikiz adaylar arasında.",
   "foto_ipucu": "Turuncu huni şeklinde şapka, alt yüz net değil",
   "mantar_olma_olasiligi": 0.98,
   "simule_top5": [
    {
     "latin_name": "Cantharellus cibarius",
     "p": 0.78
    },
    {
     "latin_name": "Omphalotus olearius",
     "p": 0.14
    },
    {
     "latin_name": "Lactarius deliciosus",
     "p": 0.04
    },
    {
     "latin_name": "Cortinarius orellanus",
     "p": 0.02
    },
    {
     "latin_name": "Boletus edulis",
     "p": 0.02
    }
   ],
   "beklenen_seviye": "KIRMIZI"
  },
  {
   "id": "c4",
   "baslik": "Kuzugöbeği + sahte kuzugöbeği",
   "aciklama": "İlkbaharda bulunan petekli/kıvrımlı şapkalı mantar.",
   "foto_ipucu": "Kahverengi kıvrımlı şapka, kesit fotoğrafı yok",
   "mantar_olma_olasiligi": 0.96,
   "simule_top5": [
    {
     "latin_name": "Morchella esculenta",
     "p": 0.7
    },
    {
     "latin_name": "Gyromitra esculenta",
     "p": 0.22
    },
    {
     "latin_name": "Boletus edulis",
     "p": 0.03
    },
    {
     "latin_name": "Coprinus comatus",
     "p": 0.03
    },
    {
     "latin_name": "Agaricus campestris",
     "p": 0.02
    }
   ],
   "beklenen_seviye": "KIRMIZI"
  },
  {
   "id": "c5",
   "baslik": "Bulanık fotoğraf",
   "aciklama": "Odaklanmamış, uzaktan çekilmiş fotoğraf. Hiçbir aday baskın değil.",
   "foto_ipucu": "Bulanık, kahverengimsi bir şekil",
   "mantar_olma_olasiligi": 0.81,
   "simule_top5": [
    {
     "latin_name": "Agaricus campestris",
     "p": 0.28
    },
    {
     "latin_name": "Boletus edulis",
     "p": 0.22
    },
    {
     "latin_name": "Macrolepiota procera",
     "p": 0.2
    },
    {
     "latin_name": "Lactarius deliciosus",
     "p": 0.18
    },
    {
     "latin_name": "Pleurotus ostreatus",
     "p": 0.12
    }
   ],
   "beklenen_seviye": "SARI"
  },
  {
   "id": "c6",
   "baslik": "Taş / kozalak fotoğrafı",
   "aciklama": "Kullanıcı yanlışlıkla bir kozalak fotoğrafı yüklüyor.",
   "foto_ipucu": "Çam kozalağı, toprak zemin",
   "mantar_olma_olasiligi": 0.12,
   "simule_top5": [
    {
     "latin_name": "Boletus edulis",
     "p": 0.35
    },
    {
     "latin_name": "Morchella esculenta",
     "p": 0.25
    },
    {
     "latin_name": "Lactarius deliciosus",
     "p": 0.2
    },
    {
     "latin_name": "Gyromitra esculenta",
     "p": 0.12
    },
    {
     "latin_name": "Pleurotus ostreatus",
     "p": 0.08
    }
   ],
   "beklenen_seviye": "MANTAR_DEGIL"
  },
  {
   "id": "c7",
   "baslik": "Peri halkası + zehirli çayır hunisi",
   "aciklama": "Çimenlikte halka şeklinde dizilmiş küçük açık renkli mantarlar. Aynı çayırda gerçekçi karışıklık.",
   "foto_ipucu": "Küçük bej şapkalar, çimen, halka düzeni",
   "mantar_olma_olasiligi": 0.95,
   "simule_top5": [
    {
     "latin_name": "Marasmius oreades",
     "p": 0.58
    },
    {
     "latin_name": "Clitocybe rivulosa",
     "p": 0.3
    },
    {
     "latin_name": "Agaricus campestris",
     "p": 0.06
    },
    {
     "latin_name": "Coprinus comatus",
     "p": 0.04
    },
    {
     "latin_name": "Macrolepiota procera",
     "p": 0.02
    }
   ],
   "beklenen_seviye": "KIRMIZI"
  },
  {
   "id": "c8",
   "baslik": "İstiridye mantarı (%88)",
   "aciklama": "Kayın gövdesinde raf şeklinde dizilmiş mantarlar. Düşük riskli aday; ama sistem yine de 'güvenli' demez.",
   "foto_ipucu": "Gri-bej istiridye şekilli şapkalar, ağaç gövdesi",
   "mantar_olma_olasiligi": 0.98,
   "simule_top5": [
    {
     "latin_name": "Pleurotus ostreatus",
     "p": 0.88
    },
    {
     "latin_name": "Lactarius deliciosus",
     "p": 0.04
    },
    {
     "latin_name": "Agaricus campestris",
     "p": 0.03
    },
    {
     "latin_name": "Coprinus comatus",
     "p": 0.03
    },
    {
     "latin_name": "Marasmius oreades",
     "p": 0.02
    }
   ],
   "beklenen_seviye": "GRI"
  }
 ]
};
window.MYCO_SPECIES = [
 {
  "id": "s01",
  "latin_name": "Amanita phalloides",
  "turkce_ad": "Köygöçüren (Yeşil köygöçüren)",
  "risk": "olumcul",
  "zehir_notu": "Amatoksin içerir; karaciğer ve böbrek yetmezliği yapar. Pişirmekle zehir yok olmaz. Mantar zehirlenmesi ölümlerinin büyük kısmından sorumludur.",
  "belirti_baslangici": "6-24 saat (gecikmeli); belirtiler geçici olarak düzelip sonra ağırlaşabilir",
  "habitat": "Meşe, kayın, kestane gibi yapraklı ağaçların altı; ormanlar ve parklar",
  "substrat": "Toprak (ağaç kökleriyle ortak yaşar)",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Agaricus campestris;Amanita rubescens;Macrolepiota procera",
  "ayirt_edici_ipucu": "Sap tabanında torba (volva) ve sapta halka bulunur; lameller hep beyaz kalır. Sap tabanını kazıyarak çıkarıp fotoğraflayın.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s02",
  "latin_name": "Galerina marginata",
  "turkce_ad": "Kenarlı galerina (Ölümcül galerina)",
  "risk": "olumcul",
  "zehir_notu": "Köygöçüren ile aynı amatoksinleri içerir; karaciğer hasarı yapar.",
  "belirti_baslangici": "6-24 saat (gecikmeli)",
  "habitat": "İğne ve yapraklı ormanlar; çürüyen kütükler",
  "substrat": "Çürük odun",
  "mevsim": "Sonbahar (ılıman kışlarda kışın da)",
  "ikiz_turler": "Kuehneromyces mutabilis;Armillaria mellea",
  "ayirt_edici_ipucu": "Küçük, kahverengi, sapta ince halka; pas kahvesi spor izi. Odun üzerinde kümeler halinde biten küçük kahverengi mantarları toplamayın.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s03",
  "latin_name": "Cortinarius orellanus",
  "turkce_ad": "Dağ örümcekağı mantarı",
  "risk": "olumcul",
  "zehir_notu": "Orellanin içerir; kalıcı böbrek hasarı yapabilir.",
  "belirti_baslangici": "2-20 gün (çok gecikmeli); bu yüzden mantarla ilişkilendirilmeyebilir",
  "habitat": "Meşe ve kayın ormanları, asitli topraklar",
  "substrat": "Toprak",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Cantharellus cibarius",
  "ayirt_edici_ipucu": "Turuncu-kahverengi şapka, pas rengi lameller ve spor izi; genç örneklerde örümcek ağı benzeri perde.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s04",
  "latin_name": "Amanita muscaria",
  "turkce_ad": "Sinek mantarı (Kırmızı benekli amanita)",
  "risk": "yuksek",
  "zehir_notu": "İbotenik asit ve muskimol içerir; bilinç bulanıklığı, halüsinasyon, kusma yapar.",
  "belirti_baslangici": "30 dakika - 3 saat",
  "habitat": "Huş ve çam ormanları",
  "substrat": "Toprak (ağaç kökleriyle ortak yaşar)",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Amanita caesarea",
  "ayirt_edici_ipucu": "Kırmızı şapka üzerinde beyaz siğiller (yağmurla silinebilir), beyaz lameller, sap tabanında halkalı yumru.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s05",
  "latin_name": "Amanita pantherina",
  "turkce_ad": "Panter mantarı",
  "risk": "yuksek",
  "zehir_notu": "Sinek mantarına benzer ama daha güçlü; ağır nörolojik belirtiler yapar.",
  "belirti_baslangici": "30 dakika - 3 saat",
  "habitat": "Yapraklı ve iğne yapraklı ormanlar",
  "substrat": "Toprak",
  "mevsim": "Yaz - Sonbahar",
  "ikiz_turler": "Amanita rubescens",
  "ayirt_edici_ipucu": "Kahverengi şapka üzerinde beyaz siğiller; et kesilince kızarmaz (Amanita rubescens kızarır). Sap tabanında belirgin kenarlı yumru.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s06",
  "latin_name": "Gyromitra esculenta",
  "turkce_ad": "Sahte kuzugöbeği (Beyin mantarı)",
  "risk": "yuksek",
  "zehir_notu": "Giromitrin içerir; karaciğer, kan ve sinir sistemi hasarı yapabilir. Pişirme buharı bile zararlı olabilir.",
  "belirti_baslangici": "6-12 saat",
  "habitat": "Çam ormanları, kumlu topraklar",
  "substrat": "Toprak / çürük odun yakını",
  "mevsim": "İlkbahar",
  "ikiz_turler": "Morchella esculenta",
  "ayirt_edici_ipucu": "Şapka beyin kıvrımı gibi düzensiz loblu, petek gözleri yok. Boyuna kesilince içi pamuksu bölmeli; gerçek kuzugöbeğinin içi tamamen boştur.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s07",
  "latin_name": "Omphalotus olearius",
  "turkce_ad": "Zeytin mantarı (Turuncu huni)",
  "risk": "yuksek",
  "zehir_notu": "İlludin içerir; şiddetli kusma ve ishal yapar.",
  "belirti_baslangici": "30 dakika - 3 saat",
  "habitat": "Zeytin, meşe ve kestane ağaçlarının dibi; Akdeniz ve Ege",
  "substrat": "Odun / kök (kümeler halinde)",
  "mevsim": "Sonbahar",
  "ikiz_turler": "Cantharellus cibarius",
  "ayirt_edici_ipucu": "Kümeler halinde odun üzerinde çıkar; gerçek lameller vardır (horoz mantarında kırışık damarlar vardır). Lameller sapa doğru uzanır, et turuncudur.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s08",
  "latin_name": "Clitocybe rivulosa",
  "turkce_ad": "Zehirli çayır hunisi",
  "risk": "yuksek",
  "zehir_notu": "Muskarin içerir; terleme, salya artışı, göz bebeği küçülmesi, solunum sıkıntısı.",
  "belirti_baslangici": "15 dakika - 2 saat",
  "habitat": "Çayırlar, çimenlikler, parklar (peri halkası oluşturabilir)",
  "substrat": "Toprak / çim",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Marasmius oreades;Clitopilus prunulus",
  "ayirt_edici_ipucu": "Beyazımsı, unlu görünümlü şapka; sık lameller sapa doğru iner. Peri halkası mantarıyla aynı çayırda çıkabilir.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s09",
  "latin_name": "Entoloma sinuatum",
  "turkce_ad": "Kurşuni pembe yaprak",
  "risk": "yuksek",
  "zehir_notu": "Ağır sindirim sistemi zehirlenmesi; karaciğerde hasar raporları var.",
  "belirti_baslangici": "30 dakika - 4 saat",
  "habitat": "Yapraklı ormanlar, kireçli topraklar",
  "substrat": "Toprak",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Clitocybe nebularis;Agaricus campestris",
  "ayirt_edici_ipucu": "Lameller genç iken sarımsı, olgunlukta pembeleşir; pembe spor izi. Un kokusu.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s10",
  "latin_name": "Amanita rubescens",
  "turkce_ad": "Kızaran amanita",
  "risk": "orta",
  "zehir_notu": "Çiğken kan hücrelerine zarar veren madde içerir. En önemli risk: ölümcül panter mantarıyla karışır.",
  "belirti_baslangici": "Çiğ yenirse 1-6 saat",
  "habitat": "Yapraklı ve iğne yapraklı ormanlar",
  "substrat": "Toprak",
  "mevsim": "Yaz - Sonbahar",
  "ikiz_turler": "Amanita pantherina;Amanita phalloides",
  "ayirt_edici_ipucu": "Et kesildiğinde ya da böcek yeniğinde pembe-kırmızıya döner. Sapta çizgili halka.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s11",
  "latin_name": "Agaricus xanthodermus",
  "turkce_ad": "Sarı lekeli kuzu mantarı",
  "risk": "orta",
  "zehir_notu": "Birçok kişide kusma, ishal ve karın ağrısı yapar.",
  "belirti_baslangici": "1-6 saat",
  "habitat": "Parklar, bahçeler, orman kenarları",
  "substrat": "Toprak",
  "mevsim": "Yaz - Sonbahar",
  "ikiz_turler": "Agaricus campestris;Agaricus arvensis",
  "ayirt_edici_ipucu": "Sap tabanı kesilince ya da şapka çizilince parlak krom sarısına döner; fenol/mürekkep kokusu.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s12",
  "latin_name": "Morchella esculenta",
  "turkce_ad": "Kuzugöbeği",
  "risk": "orta",
  "zehir_notu": "Çiğ veya az pişmiş yenirse zehirlenme yapar. Ölümcül sahte kuzugöbeği ile karışır.",
  "belirti_baslangici": "Çiğ/az pişmiş yenirse 1-12 saat",
  "habitat": "Yanmış alanlar, meyve bahçeleri, dişbudak ve karaağaç altı",
  "substrat": "Toprak",
  "mevsim": "İlkbahar",
  "ikiz_turler": "Gyromitra esculenta",
  "ayirt_edici_ipucu": "Şapka bal peteği gibi düzenli çukurlu; boyuna kesilince şapkadan sapa kadar içi tamamen boş ve tek odacıklıdır.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s13",
  "latin_name": "Agaricus campestris",
  "turkce_ad": "Çayır mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. 'Düşük risk' güvenli demek değildir; ölümcül beyaz amanitalarla karıştırılır.",
  "belirti_baslangici": "—",
  "habitat": "Otlaklar, meralar, çayırlar (ağaç olmayan alanlar)",
  "substrat": "Toprak / çim",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Amanita phalloides;Agaricus xanthodermus;Entoloma sinuatum",
  "ayirt_edici_ipucu": "Lameller pembeden çikolata kahvesine döner (amanitalarda hep beyazdır); sap tabanında torba yoktur.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s14",
  "latin_name": "Boletus edulis",
  "turkce_ad": "Ayı mantarı (Çörek mantarı)",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Acı veya kırmızı gözenekli benzerleriyle karışabilir.",
  "belirti_baslangici": "—",
  "habitat": "Çam, ladin, kayın ve meşe ormanları",
  "substrat": "Toprak (ağaç kökleriyle ortak yaşar)",
  "mevsim": "Yaz - Sonbahar",
  "ikiz_turler": "Tylopilus felleus;Rubroboletus satanas",
  "ayirt_edici_ipucu": "Lamel yerine sünger gibi gözenekler (genç iken beyaz); sapta açık renkli ağ deseni; et kesilince renk değiştirmez.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s15",
  "latin_name": "Cantharellus cibarius",
  "turkce_ad": "Horoz mantarı (Sarıkız)",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Zehirli zeytin mantarı ve örümcekağı mantarlarıyla karışır.",
  "belirti_baslangici": "—",
  "habitat": "Kayın, meşe ve çam ormanları",
  "substrat": "Toprak (tek tek veya dağınık)",
  "mevsim": "Yaz - Sonbahar",
  "ikiz_turler": "Omphalotus olearius;Hygrophoropsis aurantiaca;Cortinarius orellanus",
  "ayirt_edici_ipucu": "Gerçek lamel yok; sapa inen kalın, çatallı, kırışık damarlar. Topraktan tek tek çıkar, odun üzerinde kümeler yapmaz.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s16",
  "latin_name": "Lactarius deliciosus",
  "turkce_ad": "Çıntar",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Beyaz/acı süt salgılayan Lactarius türleriyle karışır.",
  "belirti_baslangici": "—",
  "habitat": "Çam ormanları",
  "substrat": "Toprak (çam kökleriyle)",
  "mevsim": "Sonbahar",
  "ikiz_turler": "Lactarius torminosus;Lactarius deterrimus",
  "ayirt_edici_ipucu": "Kesilince turuncu-havuç rengi süt salgılar; ezilen yerler yeşillenir. Beyaz süt salgılıyorsa bu tür değildir.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s17",
  "latin_name": "Macrolepiota procera",
  "turkce_ad": "Nar mantarı (Şemsiye mantarı)",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Küçük Lepiota türleri ve beyaz amanitalar ölümcül olabilir.",
  "belirti_baslangici": "—",
  "habitat": "Orman kenarları, açıklıklar, çayırlar",
  "substrat": "Toprak",
  "mevsim": "Yaz sonu - Sonbahar",
  "ikiz_turler": "Chlorophyllum molybdites;Amanita phalloides;Lepiota brunneoincarnata",
  "ayirt_edici_ipucu": "Çok büyük (şapka 10-30 cm); yılan derisi desenli uzun sap; sap üzerinde kaydırılabilen çift halka; sap tabanında torba yok.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s18",
  "latin_name": "Marasmius oreades",
  "turkce_ad": "Peri halkası mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Aynı çayırda zehirli Clitocybe türleriyle birlikte çıkabilir.",
  "belirti_baslangici": "—",
  "habitat": "Çayırlar, çimenlikler (halka şeklinde dizilir)",
  "substrat": "Toprak / çim",
  "mevsim": "İlkbahar sonu - Sonbahar",
  "ikiz_turler": "Clitocybe rivulosa",
  "ayirt_edici_ipucu": "Seyrek, sapa bağlanmayan lameller; sert, bükülünce kırılmayan esnek sap; kuruyup suyla yeniden canlanır.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s19",
  "latin_name": "Pleurotus ostreatus",
  "turkce_ad": "İstiridye mantarı (Kayın mantarı)",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Odun üzerinde çıkan zehirli türlerle (ör. zeytin mantarı) karışabilir.",
  "belirti_baslangici": "—",
  "habitat": "Kayın, kavak, söğüt gibi yapraklı ağaçların gövdesi",
  "substrat": "Ölü / zayıf odun (raf şeklinde)",
  "mevsim": "Sonbahar - Kış",
  "ikiz_turler": "Omphalotus olearius;Pleurocybella porrigens",
  "ayirt_edici_ipucu": "Yan yana raf gibi dizilen istiridye şeklinde şapkalar; kısa yan sap; beyaz-leylak spor izi.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 },
 {
  "id": "s20",
  "latin_name": "Coprinus comatus",
  "turkce_ad": "Mürekkep mantarı (Saçlı mürekkep)",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Benzeri Coprinopsis atramentaria alkolle birlikte alınınca zehirlenme yapar.",
  "belirti_baslangici": "—",
  "habitat": "Çimenlikler, yol kenarları, çöplük ve dolgu alanları",
  "substrat": "Toprak",
  "mevsim": "İlkbahar - Sonbahar",
  "ikiz_turler": "Coprinopsis atramentaria",
  "ayirt_edici_ipucu": "Uzun silindirik pullu beyaz şapka; yaşlandıkça lameller siyah mürekkebe dönüşerek erir.",
  "dogrulama_durumu": "TASLAK",
  "kaynak": "DOĞRULANACAK"
 }
];
