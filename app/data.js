// OTOMATİK ÜRETİLDİ: python src/build_app_data.py — elle düzenlemeyin.
window.MYCO_CASES = {
 "aciklama": "MycoGuard karar katmanı için 8 örnek vaka. Model çıktıları örnek değerlerdir; gerçek fotoğraf analizi app/model ile yapılır.",
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
     "latin_name": "Hydnum repandum",
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
   "baslik": "Çayır mantarı + kurşuni pembe yaprak",
   "aciklama": "Yayla çayırında bulunan açık renkli mantar. Birinci tahmin zararsız görünüyor ama ağır zehirlenme yapan Entoloma adaylar arasında.",
   "foto_ipucu": "Beyazımsı şapka, çayır kenarı, lameller soluk pembe",
   "mantar_olma_olasiligi": 0.95,
   "simule_top5": [
    {
     "latin_name": "Agaricus campestris",
     "p": 0.55
    },
    {
     "latin_name": "Entoloma sinuatum",
     "p": 0.25
    },
    {
     "latin_name": "Marasmius oreades",
     "p": 0.1
    },
    {
     "latin_name": "Agaricus xanthodermus",
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
  "yerel_ad": "Köygöçüren; Zehirli yumurta mantarı",
  "risk": "olumcul",
  "zehir_notu": "Amatoksin içerir; karaciğer ve böbrek yetmezliği yapar. Pişirmek, kurutmak, dondurmak zehri yok etmez. Tek bir şapka bir yetişkini öldürebilir.",
  "belirtiler": "6-24 saat belirtisiz dönem; sonra şiddetli kusma, sulu ishal, karın ağrısı, susuzluk. 1-2 gün sonra geçici 'iyileşme' hissi; ardından sarılık, kanama, karaciğer ve böbrek yetmezliği.",
  "belirti_baslangici": "6-24 saat (gecikmeli); belirtiler geçici olarak düzelip sonra ağırlaşır",
  "belirti_saat_min": "6",
  "belirti_saat_max": "24",
  "ilk_yardim_notu": "Belirti beklemeden 112 / 114. Geç başlayan (6 saatten sonra) kusma-ishal bu türü düşündürür; hastaneye mantar örneğiyle gidin. Aynı yemeği yiyen herkes başvurmalı.",
  "habitat": "Meşe, kayın, kestane, gürgen gibi yapraklı ağaçların altı; ormanlar ve parklar",
  "substrat": "Toprak (ağaç kökleriyle ortak yaşar - mikorizal)",
  "kastamonu_notu": "Küre Dağları ve kıyı ilçelerinin (Cide, İnebolu, Abana) meşe-kestane-kayın ormanlarında beklenir. Kastamonu'da yumurta mantarı toplarken karıştırılma riski yüksek.",
  "sapka_cm": "5-15",
  "sap_cm": "8-15",
  "yetisme_sureci": "Miselyumu ağaç kökleriyle yıllarca yaşar. Yaz sonu-sonbahar yağmurlarından ~1-2 hafta sonra beyaz bir 'yumurta' (torba) içinden çıkar, 3-7 günde şemsiye gibi açılır.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "8;9;10;11",
  "toplama_notu": "Toplanmaz. Diğer mantarlarla aynı sepete konmamalı; dokunduktan sonra eller yıkanmalı.",
  "ikiz_turler": "Amanita caesarea;Agaricus campestris;Amanita rubescens;Macrolepiota procera",
  "ayirt_edici_ipucu": "Sap tabanında torba (volva) ve sapta halka bulunur; lameller hep beyaz kalır. Sap tabanını kazıyarak çıkarıp fotoğraflayın. Yumurta mantarından farkı: lameller ve sap sarı değil beyazdır.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s02",
  "latin_name": "Galerina marginata",
  "turkce_ad": "Kenarlı galerina (Ölümcül galerina)",
  "yerel_ad": "—",
  "risk": "olumcul",
  "zehir_notu": "Köygöçüren ile aynı amatoksinleri içerir; karaciğer hasarı yapar.",
  "belirtiler": "6-24 saat sonra kusma, ishal, karın ağrısı; ardından karaciğer hasarı.",
  "belirti_baslangici": "6-24 saat (gecikmeli)",
  "belirti_saat_min": "6",
  "belirti_saat_max": "24",
  "ilk_yardim_notu": "Belirti beklemeden 112 / 114.",
  "habitat": "İğne ve yapraklı ormanlar; çürüyen kütükler ve dallar",
  "substrat": "Çürük odun (saprotrof)",
  "kastamonu_notu": "Göknar ve çam kütüklerinde, kesim alanlarında beklenir; odun üzerinde kümelenen küçük kahverengi mantarlarla karışır.",
  "sapka_cm": "1-5",
  "sap_cm": "2-8",
  "yetisme_sureci": "Çürüyen odunu ayrıştırır; nemli dönemlerde kümeler halinde birkaç günde çıkar.",
  "mevsim": "Sonbahar (ılık kışlarda kışın da)",
  "aylar": "9;10;11;12",
  "toplama_notu": "Toplanmaz. Odun üzerinde biten küçük kahverengi mantarlar hiç toplanmamalı.",
  "ikiz_turler": "Armillaria mellea;Hypholoma fasciculare",
  "ayirt_edici_ipucu": "Küçük, bal-kahve şapka; sapta ince halka; pas kahvesi spor izi.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s03",
  "latin_name": "Lepiota brunneoincarnata",
  "turkce_ad": "Pembe kahve lepiota",
  "yerel_ad": "—",
  "risk": "olumcul",
  "zehir_notu": "Amatoksin içerir. Küçük ve masum görünür; çayır ve bahçelerde çıkar.",
  "belirtiler": "6-24 saat sonra kusma, ishal; ardından karaciğer hasarı.",
  "belirti_baslangici": "6-24 saat (gecikmeli)",
  "belirti_saat_min": "6",
  "belirti_saat_max": "24",
  "ilk_yardim_notu": "Belirti beklemeden 112 / 114.",
  "habitat": "Çayırlar, bahçeler, park ve orman kenarları",
  "substrat": "Toprak (saprotrof)",
  "kastamonu_notu": "Köy çevresindeki çayır ve bahçelerde beklenir; küçük şemsiye mantarlarla karışır.",
  "sapka_cm": "2-5",
  "sap_cm": "2-5",
  "yetisme_sureci": "Toprakta ölü bitki artıklarını ayrıştırır; sonbahar ve ilkbahar yağmurlarıyla çıkar.",
  "mevsim": "İlkbahar ve Sonbahar",
  "aylar": "4;5;9;10;11",
  "toplama_notu": "Toplanmaz. Şapkası 10 cm'den küçük şemsiye görünümlü mantarlar toplanmamalı.",
  "ikiz_turler": "Macrolepiota procera;Agaricus campestris",
  "ayirt_edici_ipucu": "Küçük (şapka 2-5 cm); şapkada pembe-kahve pullar; sapta kuşak şeklinde pullar. Nar mantarından çok daha küçüktür.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s04",
  "latin_name": "Amanita muscaria",
  "turkce_ad": "Sinek mantarı (Kırmızı benekli amanita)",
  "yerel_ad": "Sinek mantarı",
  "risk": "yuksek",
  "zehir_notu": "İbotenik asit ve muskimol içerir; sinir sistemini etkiler.",
  "belirtiler": "Sarhoşluk hali, baş dönmesi, kas seğirmesi, halüsinasyon, huzursuzluk, ardından derin uyku; çocuklarda nöbet.",
  "belirti_baslangici": "30 dakika - 3 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "3",
  "ilk_yardim_notu": "112 / 114. Hastayı yalnız bırakmayın; düşme ve yaralanmaya karşı koruyun.",
  "habitat": "Huş, çam ve ladin ormanları",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Ilgaz ve iç kesimlerin sarıçam-göknar ormanlarında beklenir. Yağmurla siğilleri silinince yumurta mantarıyla karışabilir.",
  "sapka_cm": "8-20",
  "sap_cm": "10-25",
  "yetisme_sureci": "Mikorizal; yaz sonu-sonbahar yağmurlarından sonra yumru içinden çıkar.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "8;9;10;11",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Amanita caesarea",
  "ayirt_edici_ipucu": "Kırmızı şapka üzerinde beyaz siğiller (yağmurla silinebilir), BEYAZ lameller ve sap, sap tabanında halkalı yumru. Yumurta mantarında lameller ve sap sarıdır, torba beyaz kese şeklindedir.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s05",
  "latin_name": "Amanita pantherina",
  "turkce_ad": "Panter mantarı",
  "yerel_ad": "—",
  "risk": "yuksek",
  "zehir_notu": "Sinek mantarına benzer ama daha güçlü; ağır nörolojik belirtiler yapar.",
  "belirtiler": "Baş dönmesi, sarhoşluk, kas kasılmaları, halüsinasyon, ajitasyon; ağır vakalarda koma.",
  "belirti_baslangici": "30 dakika - 3 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "3",
  "ilk_yardim_notu": "112 / 114.",
  "habitat": "Yapraklı ve iğne yapraklı ormanlar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Meşe ve çam ormanlarında beklenir.",
  "sapka_cm": "5-12",
  "sap_cm": "6-12",
  "yetisme_sureci": "Mikorizal; yaz-sonbahar yağmurlarından sonra çıkar.",
  "mevsim": "Yaz - Sonbahar",
  "aylar": "6;7;8;9;10",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Amanita rubescens",
  "ayirt_edici_ipucu": "Kahverengi şapka üzerinde beyaz siğiller; et kesilince kızarmaz (Amanita rubescens kızarır). Sap tabanında belirgin kenarlı yumru.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s06",
  "latin_name": "Gyromitra esculenta",
  "turkce_ad": "Sahte kuzugöbeği (Beyin mantarı)",
  "yerel_ad": "Sahte kuzugöbeği",
  "risk": "yuksek",
  "zehir_notu": "Giromitrin içerir; karaciğer, kan ve sinir sistemi hasarı yapabilir. Pişirme buharı bile zararlı olabilir.",
  "belirtiler": "Kusma, ishal, baş ağrısı, yorgunluk; ağır vakalarda nöbet ve sarılık.",
  "belirti_baslangici": "5-24 saat",
  "belirti_saat_min": "5",
  "belirti_saat_max": "24",
  "ilk_yardim_notu": "112 / 114. Pişirildiği mutfaktaki herkes buhardan etkilenmiş olabilir.",
  "habitat": "Çam ormanları, kumlu topraklar, kesim alanları",
  "substrat": "Toprak / çürük odun yakını",
  "kastamonu_notu": "İlkbaharda kuzugöbeği toplanan çam ormanlarında birlikte çıkabilir.",
  "sapka_cm": "3-10",
  "sap_cm": "2-6",
  "yetisme_sureci": "Kar erimesinden sonra ilkbaharda çıkar.",
  "mevsim": "İlkbahar",
  "aylar": "3;4;5",
  "toplama_notu": "Toplanmaz. Kuzugöbeği toplarken her örnek boyuna kesilip kontrol edilmeli.",
  "ikiz_turler": "Morchella esculenta",
  "ayirt_edici_ipucu": "Şapka beyin kıvrımı gibi düzensiz loblu, petek gözleri yok. Boyuna kesilince içi pamuksu bölmeli; gerçek kuzugöbeğinin içi tamamen boştur.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s07",
  "latin_name": "Omphalotus olearius",
  "turkce_ad": "Zeytin mantarı (Turuncu huni)",
  "yerel_ad": "—",
  "risk": "yuksek",
  "zehir_notu": "İlludin içerir; şiddetli kusma ve ishal yapar.",
  "belirtiler": "Şiddetli kusma, ishal, karın krampları, halsizlik.",
  "belirti_baslangici": "30 dakika - 3 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "3",
  "ilk_yardim_notu": "114'ü arayın; sıvı kaybına karşı hastaneye başvurun.",
  "habitat": "Zeytin, meşe ve kestane ağaçlarının dibi",
  "substrat": "Odun / kök (kümeler halinde)",
  "kastamonu_notu": "Kıyı ilçelerinin (Cide, İnebolu, Abana) kestane ve meşe ağaçlarının dibinde beklenir; sarıkızla karışır.",
  "sapka_cm": "5-15",
  "sap_cm": "5-15",
  "yetisme_sureci": "Ağaç kökü ve kütükleri ayrıştırır; sonbaharda kümeler halinde çıkar.",
  "mevsim": "Sonbahar",
  "aylar": "9;10;11;12",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Cantharellus cibarius",
  "ayirt_edici_ipucu": "Kümeler halinde odun üzerinde çıkar; gerçek bıçak gibi lameller vardır (sarıkızda kırışık damarlar vardır). Et içi de turuncudur.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s08",
  "latin_name": "Entoloma sinuatum",
  "turkce_ad": "Kurşuni pembe yaprak",
  "yerel_ad": "—",
  "risk": "yuksek",
  "zehir_notu": "Ağır sindirim sistemi zehirlenmesi; karaciğerde hasar raporları var.",
  "belirtiler": "Şiddetli kusma, ishal, karın ağrısı; günlerce sürebilir.",
  "belirti_baslangici": "30 dakika - 4 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "4",
  "ilk_yardim_notu": "114 / hastane; sıvı kaybı tehlikelidir.",
  "habitat": "Yapraklı ormanlar, kireçli topraklar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Meşe-kayın ormanlarında beklenir.",
  "sapka_cm": "6-20",
  "sap_cm": "5-15",
  "yetisme_sureci": "Mikorizal; yaz sonu-sonbahar.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "8;9;10",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Agaricus campestris",
  "ayirt_edici_ipucu": "Lameller genç iken sarımsı, olgunlukta pembeleşir; pembe spor izi. Un kokusu.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s09",
  "latin_name": "Hypholoma fasciculare",
  "turkce_ad": "Kükürt mantarı (Kükürt başlı)",
  "yerel_ad": "—",
  "risk": "yuksek",
  "zehir_notu": "Sindirim sistemi zehirlenmesi; nadiren ağır seyreder.",
  "belirtiler": "Kusma, ishal, terleme; nadiren karaciğer etkilenmesi.",
  "belirti_baslangici": "30 dakika - 10 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "10",
  "ilk_yardim_notu": "114'ü arayın.",
  "habitat": "Yapraklı ve iğne yapraklı ormanlar; kütükler",
  "substrat": "Çürük odun (yoğun kümeler)",
  "kastamonu_notu": "Kastamonu ormanlarında kütükler üzerinde çok yaygın olması beklenir; bal mantarı ile karışır.",
  "sapka_cm": "2-7",
  "sap_cm": "4-10",
  "yetisme_sureci": "Ölü odunu ayrıştırır; nemli dönemlerde hemen her ay kümeler yapabilir.",
  "mevsim": "Yıl boyu (en çok sonbahar)",
  "aylar": "1;2;3;4;5;6;7;8;9;10;11;12",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Armillaria mellea;Galerina marginata",
  "ayirt_edici_ipucu": "Kükürt sarısı şapka ve sap; lameller yeşilimsi-sarı, sonra mor-kahve. Acı tat. Yoğun kümeler halinde kütükte.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s10",
  "latin_name": "Rubroboletus satanas",
  "turkce_ad": "Şeytan mantarı",
  "yerel_ad": "—",
  "risk": "yuksek",
  "zehir_notu": "Pişmiş halde bile şiddetli sindirim zehirlenmesi yapar.",
  "belirtiler": "Şiddetli kusma, ishal, karın krampları.",
  "belirti_baslangici": "30 dakika - 5 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "5",
  "ilk_yardim_notu": "114 / hastane.",
  "habitat": "Meşe, kayın, kestane ormanları; kireçli topraklar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Meşe ve kestane ormanlarında beklenir; ayı mantarıyla karışır.",
  "sapka_cm": "10-30",
  "sap_cm": "5-15",
  "yetisme_sureci": "Mikorizal; sıcak yaz yağmurlarından sonra.",
  "mevsim": "Yaz",
  "aylar": "6;7;8;9",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Boletus edulis",
  "ayirt_edici_ipucu": "Beyazımsı-gri şapka, KIRMIZI gözenekler, kırmızı ağlı şişkin sap; kesilince maviye döner. Ayı mantarının gözenekleri beyaz-sarı-yeşildir ve kesilince renk değiştirmez.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s11",
  "latin_name": "Amanita rubescens",
  "turkce_ad": "Kızaran amanita",
  "yerel_ad": "—",
  "risk": "orta",
  "zehir_notu": "Çiğken kan hücrelerine zarar veren madde içerir. En önemli risk: ölümcül panter mantarıyla karışır.",
  "belirtiler": "Çiğ yenirse kusma, karın ağrısı; kansızlık.",
  "belirti_baslangici": "Çiğ yenirse 1-6 saat",
  "belirti_saat_min": "1",
  "belirti_saat_max": "6",
  "ilk_yardim_notu": "114'ü arayın; panter mantarı olma ihtimalini bildirin.",
  "habitat": "Yapraklı ve iğne yapraklı ormanlar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Meşe ve çam ormanlarında beklenir.",
  "sapka_cm": "5-15",
  "sap_cm": "8-15",
  "yetisme_sureci": "Mikorizal; yaz-sonbahar.",
  "mevsim": "Yaz - Sonbahar",
  "aylar": "6;7;8;9;10",
  "toplama_notu": "Panter mantarıyla karıştığı için toplanması önerilmez.",
  "ikiz_turler": "Amanita pantherina;Amanita phalloides",
  "ayirt_edici_ipucu": "Et kesildiğinde ya da böcek yeniğinde pembe-kırmızıya döner. Sapta çizgili halka.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s12",
  "latin_name": "Agaricus xanthodermus",
  "turkce_ad": "Sarı lekeli kuzu mantarı",
  "yerel_ad": "—",
  "risk": "orta",
  "zehir_notu": "Birçok kişide kusma, ishal ve karın ağrısı yapar.",
  "belirtiler": "Bulantı, kusma, karın krampları, ishal.",
  "belirti_baslangici": "30 dakika - 6 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "6",
  "ilk_yardim_notu": "114'ü arayın.",
  "habitat": "Parklar, bahçeler, orman kenarları",
  "substrat": "Toprak",
  "kastamonu_notu": "Köy bahçeleri ve yol kenarlarında beklenir; çayır mantarıyla karışır.",
  "sapka_cm": "5-15",
  "sap_cm": "6-15",
  "yetisme_sureci": "Toprakta ölü organik maddeyi ayrıştırır; yaz sonu yağmurlarıyla.",
  "mevsim": "Yaz - Sonbahar",
  "aylar": "7;8;9;10",
  "toplama_notu": "Toplanmaz.",
  "ikiz_turler": "Agaricus campestris",
  "ayirt_edici_ipucu": "Sap tabanı kesilince ya da şapka çizilince parlak krom sarısına döner; fenol/mürekkep kokusu.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s13",
  "latin_name": "Morchella esculenta",
  "turkce_ad": "Kuzugöbeği",
  "yerel_ad": "Kuzugöbeği",
  "risk": "orta",
  "zehir_notu": "Çiğ veya az pişmiş yenirse zehirlenme yapar. Sahte kuzugöbeği ile karışır.",
  "belirtiler": "Çiğ/az pişmiş: bulantı, kusma, ishal; nadiren baş dönmesi.",
  "belirti_baslangici": "Çiğ/az pişmiş yenirse 1-12 saat",
  "belirti_saat_min": "1",
  "belirti_saat_max": "12",
  "ilk_yardim_notu": "114'ü arayın; sahte kuzugöbeği olma ihtimalini bildirin.",
  "habitat": "Yanmış alanlar, meyve bahçeleri, dişbudak, karaağaç ve çam altı",
  "substrat": "Toprak",
  "kastamonu_notu": "Kastamonu ilkbaharda kuzugöbeği toplanan önemli bölgelerdendir (iç ve orman ilçeleri). Sahte kuzugöbeği aynı dönemde çıkar.",
  "sapka_cm": "3-8 (şapka yüksekliği)",
  "sap_cm": "3-8",
  "yetisme_sureci": "Kar erimesi ve toprak ısınmasıyla ilkbaharda çıkar; yanmış alanlarda bol olabilir. Birkaç haftalık kısa bir dönemi vardır.",
  "mevsim": "İlkbahar",
  "aylar": "3;4;5;6",
  "toplama_notu": "İlkbahar (Mart-Haziran). Her örnek boyuna kesilip içinin boş olduğu kontrol edilmeli; tür onayı uzmana yaptırılmalı.",
  "ikiz_turler": "Gyromitra esculenta",
  "ayirt_edici_ipucu": "Şapka bal peteği gibi düzenli çukurlu; boyuna kesilince şapkadan sapa kadar içi tamamen boş ve tek odacıklıdır.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s14",
  "latin_name": "Armillaria mellea",
  "turkce_ad": "Bal mantarı (Ağaç mantarı)",
  "yerel_ad": "Ağaç mantarı",
  "risk": "orta",
  "zehir_notu": "Çiğ veya az pişmiş yenirse sindirim şikâyeti yapar; bazı kişiler pişmişine de duyarlıdır.",
  "belirtiler": "Bulantı, kusma, ishal.",
  "belirti_baslangici": "Çiğ/az pişmiş yenirse 0,5-6 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "6",
  "ilk_yardim_notu": "114'ü arayın.",
  "habitat": "Yapraklı ve iğne yapraklı ağaçların kökleri ve kütükleri",
  "substrat": "Canlı/ölü odun (parazit; kümeler halinde)",
  "kastamonu_notu": "Kastamonu ormanlarında kütük ve ağaç diplerinde yaygın olması beklenir; ölümcül galerina ve kükürt mantarıyla karışır.",
  "sapka_cm": "3-10",
  "sap_cm": "5-15",
  "yetisme_sureci": "Ağaçlara kök çürüklüğü yapan bir parazittir; siyah kordonlarla yayılır, sonbaharda kümeler halinde çıkar.",
  "mevsim": "Sonbahar",
  "aylar": "9;10;11",
  "toplama_notu": "Ölümcül galerina ile karıştığı için yalnızca uzman onayıyla.",
  "ikiz_turler": "Galerina marginata;Hypholoma fasciculare",
  "ayirt_edici_ipucu": "Bal sarısı şapkada koyu pulcuklar; sapta belirgin halka; BEYAZ spor izi (galerinada pas kahvesi). Büyük kümeler.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s15",
  "latin_name": "Agaricus campestris",
  "turkce_ad": "Çayır mantarı",
  "yerel_ad": "Kuzu mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. 'Düşük risk' güvenli demek değildir; ölümcül beyaz amanitalarla karıştırılır.",
  "belirtiler": "Genelde zehirlenme beklenmez; bozulmuş veya yanlış tanınmış mantar sindirim şikâyeti yapabilir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Otlaklar, meralar, çayırlar (ağaç olmayan alanlar)",
  "substrat": "Toprak / çim",
  "kastamonu_notu": "Yayla ve meralarda yaz sonu yağmurlarından sonra beklenir.",
  "sapka_cm": "3-10",
  "sap_cm": "3-8",
  "yetisme_sureci": "Çayır toprağında ayrıştırıcıdır; yağmurdan birkaç gün sonra hızla çıkar ve 1 hafta içinde yaşlanır.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "7;8;9;10",
  "toplama_notu": "Görülme dönemi Temmuz-Ekim. Yalnızca uzman tür onayından sonra; lameller pembe-kahve değilse hiç toplanmamalı.",
  "ikiz_turler": "Amanita phalloides;Agaricus xanthodermus;Entoloma sinuatum",
  "ayirt_edici_ipucu": "Lameller pembeden çikolata kahvesine döner (amanitalarda hep beyazdır); sap tabanında torba yoktur.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s16",
  "latin_name": "Boletus edulis",
  "turkce_ad": "Ayı mantarı (Çörek mantarı)",
  "yerel_ad": "Ayı mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Kırmızı gözenekli şeytan mantarıyla karışabilir.",
  "belirtiler": "Genelde zehirlenme beklenmez; yanlış tanıma asıl risktir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Çam, ladin, kayın ve meşe ormanları",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Küre ve Ilgaz'ın kayın-göknar-çam ormanlarında beklenir.",
  "sapka_cm": "8-25",
  "sap_cm": "8-20",
  "yetisme_sureci": "Mikorizal; ılık yağmurlardan ~10 gün sonra çıkar, birkaç günde büyür; çabuk kurtlanır.",
  "mevsim": "Yaz - Sonbahar",
  "aylar": "6;7;8;9;10",
  "toplama_notu": "Görülme dönemi Haziran-Ekim. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Rubroboletus satanas",
  "ayirt_edici_ipucu": "Lamel yerine sünger gibi gözenekler (genç iken beyaz); sapta açık renkli ağ deseni; et kesilince renk değiştirmez.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s17",
  "latin_name": "Cantharellus cibarius",
  "turkce_ad": "Sarıkız (Horoz mantarı)",
  "yerel_ad": "Sarıkız; Horoz mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Zehirli zeytin mantarı ve örümcekağı mantarlarıyla karışır.",
  "belirtiler": "Genelde zehirlenme beklenmez; yanlış tanıma asıl risktir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Kayın, meşe, kestane ve çam ormanları",
  "substrat": "Toprak (mikorizal; tek tek veya dağınık)",
  "kastamonu_notu": "Kastamonu ormanlarında en çok toplanan türlerdendir; kıyıdaki kestane-meşe ormanlarında zeytin mantarıyla karışabilir.",
  "sapka_cm": "3-10",
  "sap_cm": "3-8",
  "yetisme_sureci": "Mikorizal; yavaş büyür, aynı örnek haftalarca büyümeye devam edebilir.",
  "mevsim": "Yaz - Sonbahar",
  "aylar": "6;7;8;9;10",
  "toplama_notu": "Görülme dönemi Haziran-Ekim. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Omphalotus olearius",
  "ayirt_edici_ipucu": "Gerçek lamel yok; sapa inen kalın, çatallı, kırışık damarlar. Topraktan tek tek çıkar, odun üzerinde kümeler yapmaz.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s18",
  "latin_name": "Lactarius deliciosus",
  "turkce_ad": "Kanlıca (Çıntar)",
  "yerel_ad": "Kanlıca; Çıntar",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Beyaz/acı süt salgılayan Lactarius türleriyle karışır.",
  "belirtiler": "Genelde zehirlenme beklenmez; benzer acı türler sindirim şikâyeti yapabilir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Çam ormanları",
  "substrat": "Toprak (çam kökleriyle)",
  "kastamonu_notu": "Karaçam ve sarıçam ormanlarında sonbaharda yaygın olması beklenir.",
  "sapka_cm": "4-12",
  "sap_cm": "3-7",
  "yetisme_sureci": "Çam kökleriyle mikorizal; sonbahar yağmurlarından sonra çıkar.",
  "mevsim": "Sonbahar",
  "aylar": "9;10;11",
  "toplama_notu": "Görülme dönemi Eylül-Kasım. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Lactarius torminosus",
  "ayirt_edici_ipucu": "Kesilince turuncu-havuç rengi süt salgılar; ezilen yerler yeşillenir. Beyaz süt salgılıyorsa bu tür değildir.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s19",
  "latin_name": "Macrolepiota procera",
  "turkce_ad": "Nar mantarı (Şemsiye mantarı)",
  "yerel_ad": "Şemsiye mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Küçük Lepiota türleri ve beyaz amanitalar ölümcül olabilir.",
  "belirtiler": "Genelde zehirlenme beklenmez; yanlış tanıma asıl risktir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Orman kenarları, açıklıklar, çayırlar",
  "substrat": "Toprak",
  "kastamonu_notu": "Orman açıklıkları ve yol kenarlarında beklenir.",
  "sapka_cm": "10-30",
  "sap_cm": "15-40",
  "yetisme_sureci": "Toprakta ayrıştırıcı; yaz sonu yağmurlarıyla çıkar, 'davul tokmağı' şeklinden şemsiyeye açılır.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "7;8;9;10",
  "toplama_notu": "Görülme dönemi Temmuz-Ekim. Şapkası 10 cm'den küçükse hiç toplanmamalı; uzman onayı gerekir.",
  "ikiz_turler": "Lepiota brunneoincarnata;Amanita phalloides",
  "ayirt_edici_ipucu": "Çok büyük (şapka 10-30 cm); yılan derisi desenli uzun sap; sap üzerinde kaydırılabilen çift halka; sap tabanında torba yok.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s20",
  "latin_name": "Amanita caesarea",
  "turkce_ad": "Yumurta mantarı (Paşa mantarı)",
  "yerel_ad": "Yumurta mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Ancak yumurta (kapalı) evresinde ölümcül köygöçürenle ve siğilleri silinmiş sinek mantarıyla karışır.",
  "belirtiler": "Genelde zehirlenme beklenmez; yanlış tanıma ölümcül olabilir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa hemen 114.",
  "habitat": "Meşe ve kestane ormanları, sıcak yamaçlar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Kastamonu ve Batı Karadeniz'de sevilerek toplanan bir türdür; kıyı ilçelerinin meşe-kestane ormanlarında beklenir.",
  "sapka_cm": "8-20",
  "sap_cm": "8-15",
  "yetisme_sureci": "Mikorizal; sıcak yaz yağmurlarından sonra beyaz bir torbadan 'yumurta' gibi çıkar.",
  "mevsim": "Yaz - Sonbahar",
  "aylar": "6;7;8;9;10",
  "toplama_notu": "Görülme dönemi Haziran-Ekim. Kapalı 'yumurta' evresinde ASLA toplanmamalı (köygöçürenle ayırt edilemez); yalnızca uzman onayıyla.",
  "ikiz_turler": "Amanita phalloides;Amanita muscaria",
  "ayirt_edici_ipucu": "Turuncu-kırmızı şapka, SARI lameller ve SARI sap, beyaz kese şeklinde geniş torba. Sinek mantarında lameller ve sap beyazdır.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s21",
  "latin_name": "Hydnum repandum",
  "turkce_ad": "Kirpi mantarı",
  "yerel_ad": "—",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Belirgin ölümcül ikizi yoktur ama yine de uzman onayı gerekir.",
  "belirtiler": "Genelde zehirlenme beklenmez.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Kayın, meşe ve iğne yapraklı ormanlar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Kayın-göknar ormanlarında sonbaharda beklenir.",
  "sapka_cm": "4-12",
  "sap_cm": "3-8",
  "yetisme_sureci": "Mikorizal; sonbahar yağmurlarıyla çıkar, soğuğa dayanıklıdır.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "8;9;10;11",
  "toplama_notu": "Görülme dönemi Ağustos-Kasım. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Sarcodon imbricatus",
  "ayirt_edici_ipucu": "Şapkanın altında lamel veya gözenek yerine yumuşak, kırılgan dikenler (sarkıtlar) bulunur.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s22",
  "latin_name": "Craterellus cornucopioides",
  "turkce_ad": "Borazan mantarı (Siyah borazan)",
  "yerel_ad": "—",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir.",
  "belirtiler": "Genelde zehirlenme beklenmez.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Kayın ve meşe ormanları; nemli, yosunlu yerler",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Kayın ormanlarının nemli yamaçlarında beklenir.",
  "sapka_cm": "3-8",
  "sap_cm": "5-12",
  "yetisme_sureci": "Mikorizal; nemli sonbaharlarda gruplar halinde.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "8;9;10;11",
  "toplama_notu": "Görülme dönemi Ağustos-Kasım. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Craterellus lutescens",
  "ayirt_edici_ipucu": "Koyu gri-siyah, içi boş borazan/huni şekli; alt yüz neredeyse düz, lamelsiz.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s23",
  "latin_name": "Pleurotus ostreatus",
  "turkce_ad": "İstiridye mantarı (Kayın mantarı)",
  "yerel_ad": "Kayın mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Odun üzerinde çıkan zehirli türlerle karışabilir.",
  "belirtiler": "Genelde zehirlenme beklenmez.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Kayın, kavak, söğüt gibi yapraklı ağaçların gövdesi",
  "substrat": "Ölü / zayıf odun (raf şeklinde)",
  "kastamonu_notu": "Kayın ormanlarında soğuk aylarda beklenir.",
  "sapka_cm": "5-20",
  "sap_cm": "1-3",
  "yetisme_sureci": "Ölü odunu ayrıştırır; soğuk ve nemli havada çıkar, birkaç günde büyür.",
  "mevsim": "Sonbahar - Kış",
  "aylar": "10;11;12;1;2;3",
  "toplama_notu": "Görülme dönemi Ekim-Mart. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Omphalotus olearius",
  "ayirt_edici_ipucu": "Yan yana raf gibi dizilen istiridye şeklinde şapkalar; kısa yan sap; beyaz-leylak spor izi.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s24",
  "latin_name": "Coprinus comatus",
  "turkce_ad": "Mürekkep mantarı (Saçlı mürekkep)",
  "yerel_ad": "—",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Benzeri Coprinopsis atramentaria alkolle birlikte alınınca zehirlenme yapar.",
  "belirtiler": "Genelde zehirlenme beklenmez.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Alkolle birlikte şikâyet olursa benzer türü düşünün; 114.",
  "habitat": "Çimenlikler, yol kenarları, dolgu alanları",
  "substrat": "Toprak",
  "kastamonu_notu": "Köy ve kasaba çevresindeki yol kenarlarında beklenir.",
  "sapka_cm": "3-6",
  "sap_cm": "10-30",
  "yetisme_sureci": "Ayrıştırıcı; yağmurdan sonra birkaç saatte çıkar, 1-2 günde mürekkep gibi erir.",
  "mevsim": "İlkbahar - Sonbahar",
  "aylar": "4;5;6;7;8;9;10;11",
  "toplama_notu": "Görülme dönemi Nisan-Kasım. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Coprinopsis atramentaria",
  "ayirt_edici_ipucu": "Uzun silindirik pullu beyaz şapka; yaşlandıkça lameller siyah mürekkebe dönüşerek erir.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s25",
  "latin_name": "Marasmius oreades",
  "turkce_ad": "Peri halkası mantarı",
  "yerel_ad": "—",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Aynı çayırda ölümcül küçük Lepiota türleriyle birlikte çıkabilir.",
  "belirtiler": "Genelde zehirlenme beklenmez.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Çayırlar, çimenlikler (halka şeklinde dizilir)",
  "substrat": "Toprak / çim",
  "kastamonu_notu": "Yayla çayırlarında beklenir.",
  "sapka_cm": "2-6",
  "sap_cm": "3-10",
  "yetisme_sureci": "Çim toprağında halka şeklinde dışa doğru yayılır; yağmurdan sonra çıkar, kuruyup yeniden canlanır.",
  "mevsim": "İlkbahar sonu - Sonbahar",
  "aylar": "5;6;7;8;9;10",
  "toplama_notu": "Görülme dönemi Mayıs-Ekim. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Lepiota brunneoincarnata",
  "ayirt_edici_ipucu": "Seyrek, sapa bağlanmayan lameller; sert, bükülünce kırılmayan esnek sap; kuruyup suyla yeniden canlanır.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s26",
  "latin_name": "Ramaria spp.",
  "turkce_ad": "Saçak (Mercan mantarları)",
  "yerel_ad": "Saçak; Mercan mantarı; Keçi sakalı",
  "risk": "orta",
  "zehir_notu": "Saçak (mercan) mantarlarının bir kısmı, ör. Ramaria formosa ve Ramaria pallida, şiddetli ishal ve kusma yapar. Türler birbirinden ancak mikroskop ve kimyasal testlerle güvenilir şekilde ayrılabilir; yaşlı örnekler acılaşır.",
  "belirtiler": "Bulantı, kusma, karın krampları, sulu ishal.",
  "belirti_baslangici": "30 dakika - 4 saat",
  "belirti_saat_min": "0.5",
  "belirti_saat_max": "4",
  "ilk_yardim_notu": "114'ü arayın; sıvı kaybına dikkat edin, yaşlılarda ve çocuklarda hastaneye başvurun.",
  "habitat": "Kayın, göknar ve meşe ormanları; yaprak ve iğne döküntüsü olan topraklar",
  "substrat": "Toprak (mikorizal)",
  "kastamonu_notu": "Kastamonu'da 'saçak' adıyla toplanan dallı mercan mantarlarındandır; Kastamonu Üniversitesi çalışmalarında yörede toplanan Ramaria türleri bildirilmiştir. Benzer türler çok olduğundan en riskli toplanan gruplardandır.",
  "sapka_cm": "6-20 (küme genişliği)",
  "sap_cm": "3-8 (ortak gövde)",
  "yetisme_sureci": "Mikorizal; yaz sonu-sonbahar yağmurlarından sonra kalın beyaz bir gövdeden yukarı doğru çok sayıda ince dal çıkarır; dal uçları yaşla birlikte solar ve et acılaşır.",
  "mevsim": "Yaz sonu - Sonbahar",
  "aylar": "8;9;10;11",
  "toplama_notu": "Görülme dönemi Ağustos-Kasım. Zehirli benzerleri çok olduğundan toplanması önerilmez; yalnızca uzman onayıyla.",
  "ikiz_turler": "Ramaria formosa;Ramaria pallida;Calocera viscosa",
  "ayirt_edici_ipucu": "Şapkası yoktur; kalın beyaz bir gövdeden çıkan sarı, sık dallar mercan gibi görünür. Somon-pembe dallı ve sarı uçlu olanlar (R. formosa) ile soluk mor-krem olanlar (R. pallida) ishal yapar. Odun üzerinde çıkan küçük, yapışkan turuncu 'boynuzlar' (Calocera viscosa) ayrı bir türdür.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 },
 {
  "id": "s27",
  "latin_name": "Grifola frondosa",
  "turkce_ad": "Koçak (Koyun başı mantarı)",
  "yerel_ad": "Koçak; Koç mantarı",
  "risk": "dusuk",
  "zehir_notu": "Genel olarak zehirsiz kabul edilir. Ağaç dibinde iri kümeler yapan başka türlerle karışabilir; tür onayı uzmana yaptırılmalı.",
  "belirtiler": "Genelde zehirlenme beklenmez; bozulmuş ya da yanlış tanınmış mantar sindirim şikâyeti yapabilir.",
  "belirti_baslangici": "—",
  "belirti_saat_min": "",
  "belirti_saat_max": "",
  "ilk_yardim_notu": "Yanlış tür olabilir: şikâyet varsa 114.",
  "habitat": "Yaşlı meşe ve kestane ağaçlarının dibi, kökleri üzerinde",
  "substrat": "Canlı ağaç kökü / kütük dibi (büyük kümeler)",
  "kastamonu_notu": "Kastamonu'da 'koçak' ya da 'koç mantarı' olarak bilinir; yaşlı meşe ve kestane ağaçlarının dibinde sonbaharda iri kümeler halinde çıkması beklenir.",
  "sapka_cm": "2-7 (tek şapka); küme 15-50",
  "sap_cm": "1-3 (ortak dallı sap)",
  "yetisme_sureci": "Yaşlı meşe köklerinde yıllarca yaşar; her sonbahar aynı ağacın dibinde, yüzlerce yelpaze biçimli şapkadan oluşan büyük bir küme verir.",
  "mevsim": "Sonbahar",
  "aylar": "9;10;11",
  "toplama_notu": "Görülme dönemi Eylül-Kasım. Yalnızca uzman tür onayından sonra.",
  "ikiz_turler": "Meripilus giganteus;Bondarzewia mesenterica",
  "ayirt_edici_ipucu": "Gri-kahve, kaşık ya da yelpaze biçimli çok sayıda küçük şapka ortak, dallı bir saptan çıkar; alt yüz beyaz ve gözeneklidir. Dev yelpaze mantarı (Meripilus giganteus) daha iri şapkalıdır ve kesilince ya da ezilince kararır.",
  "dogrulama_durumu": "uzman_incelemesinde",
  "kaynak": "Genel mikoloji literatürü; GBIF Türkiye kayıtları"
 }
];
window.MYCO_GBIF = {
 "Amanita phalloides": {
  "tr": 25,
  "kastamonu": 2,
  "aylar": [
   1,
   0,
   1,
   0,
   0,
   0,
   0,
   1,
   2,
   12,
   7,
   1
  ]
 },
 "Galerina marginata": {
  "tr": 7,
  "kastamonu": 1,
  "aylar": [
   1,
   0,
   0,
   0,
   0,
   0,
   0,
   2,
   0,
   2,
   2,
   0
  ]
 },
 "Lepiota brunneoincarnata": {
  "tr": 1,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   0,
   0
  ]
 },
 "Amanita muscaria": {
  "tr": 58,
  "kastamonu": 3,
  "aylar": [
   1,
   0,
   0,
   1,
   0,
   0,
   5,
   11,
   11,
   18,
   6,
   5
  ]
 },
 "Amanita pantherina": {
  "tr": 45,
  "kastamonu": 2,
  "aylar": [
   1,
   0,
   0,
   0,
   0,
   0,
   1,
   2,
   2,
   18,
   16,
   5
  ]
 },
 "Gyromitra esculenta": {
  "tr": 18,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   1,
   9,
   5,
   0,
   0,
   0,
   0,
   2,
   0,
   0
  ]
 },
 "Omphalotus olearius": {
  "tr": 12,
  "kastamonu": 0,
  "aylar": [
   2,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   5,
   2,
   3
  ]
 },
 "Entoloma sinuatum": {
  "tr": 3,
  "kastamonu": 0,
  "aylar": [
   1,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   2,
   0
  ]
 },
 "Hypholoma fasciculare": {
  "tr": 37,
  "kastamonu": 1,
  "aylar": [
   0,
   4,
   3,
   2,
   0,
   2,
   0,
   1,
   0,
   14,
   7,
   3
  ]
 },
 "Rubroboletus satanas": {
  "tr": 2,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   0,
   0
  ]
 },
 "Amanita rubescens": {
  "tr": 33,
  "kastamonu": 0,
  "aylar": [
   1,
   0,
   2,
   0,
   0,
   5,
   6,
   4,
   3,
   4,
   6,
   1
  ]
 },
 "Agaricus xanthodermus": {
  "tr": 6,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   0,
   0,
   1,
   0,
   0,
   0,
   0,
   2,
   3,
   0
  ]
 },
 "Morchella esculenta": {
  "tr": 11,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   2,
   5,
   3,
   1,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 },
 "Armillaria mellea": {
  "tr": 35,
  "kastamonu": 0,
  "aylar": [
   3,
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   0,
   8,
   10,
   11
  ]
 },
 "Agaricus campestris": {
  "tr": 10,
  "kastamonu": 0,
  "aylar": [
   1,
   0,
   0,
   0,
   0,
   1,
   1,
   0,
   0,
   3,
   1,
   3
  ]
 },
 "Boletus edulis": {
  "tr": 13,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   2,
   0,
   0,
   2,
   0,
   1,
   2,
   5,
   0,
   0
  ]
 },
 "Cantharellus cibarius": {
  "tr": 14,
  "kastamonu": 1,
  "aylar": [
   1,
   0,
   0,
   0,
   0,
   2,
   1,
   3,
   3,
   1,
   1,
   1
  ]
 },
 "Lactarius deliciosus": {
  "tr": 36,
  "kastamonu": 1,
  "aylar": [
   11,
   0,
   0,
   0,
   1,
   2,
   3,
   1,
   1,
   5,
   4,
   7
  ]
 },
 "Macrolepiota procera": {
  "tr": 48,
  "kastamonu": 3,
  "aylar": [
   3,
   0,
   0,
   1,
   3,
   3,
   3,
   2,
   3,
   18,
   5,
   7
  ]
 },
 "Amanita caesarea": {
  "tr": 44,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   0,
   0,
   0,
   2,
   2,
   3,
   11,
   19,
   6,
   1
  ]
 },
 "Hydnum repandum": {
  "tr": 9,
  "kastamonu": 0,
  "aylar": [
   3,
   0,
   0,
   0,
   0,
   0,
   0,
   1,
   2,
   1,
   1,
   1
  ]
 },
 "Craterellus cornucopioides": {
  "tr": 16,
  "kastamonu": 0,
  "aylar": [
   2,
   0,
   1,
   0,
   0,
   0,
   0,
   2,
   2,
   4,
   3,
   2
  ]
 },
 "Pleurotus ostreatus": {
  "tr": 37,
  "kastamonu": 0,
  "aylar": [
   2,
   2,
   3,
   1,
   0,
   0,
   0,
   0,
   1,
   6,
   12,
   9
  ]
 },
 "Coprinus comatus": {
  "tr": 129,
  "kastamonu": 0,
  "aylar": [
   2,
   1,
   1,
   17,
   30,
   4,
   1,
   0,
   4,
   28,
   25,
   16
  ]
 },
 "Marasmius oreades": {
  "tr": 10,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   0,
   1,
   1,
   0,
   0,
   0,
   1,
   2,
   3,
   2
  ]
 },
 "Ramaria spp.": {
  "tr": 7,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   2,
   0,
   0,
   0,
   0,
   0,
   0,
   4,
   0,
   0
  ]
 },
 "Grifola frondosa": {
  "tr": 0,
  "kastamonu": 0,
  "aylar": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 }
};
window.MYCO_THUMBS = {
 "Amanita phalloides": {
  "src": "img/sp/s01.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/315054013"
 },
 "Galerina marginata": {
  "src": "img/sp/s02.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/254400003"
 },
 "Lepiota brunneoincarnata": {
  "src": "img/sp/s03.jpg",
  "atif": "(c) vuikaan, some rights reserved (CC BY)",
  "lisans": "cc-by",
  "kaynak": "https://www.inaturalist.org/observations/181183977"
 },
 "Amanita muscaria": {
  "src": "img/sp/s04.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/246329501"
 },
 "Amanita pantherina": {
  "src": "img/sp/s05.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/121146645"
 },
 "Gyromitra esculenta": {
  "src": "img/sp/s06.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/22103341"
 },
 "Omphalotus olearius": {
  "src": "img/sp/s07.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/38640295"
 },
 "Entoloma sinuatum": {
  "src": "img/sp/s08.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/247091652"
 },
 "Hypholoma fasciculare": {
  "src": "img/sp/s09.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/117101166"
 },
 "Rubroboletus satanas": {
  "src": "img/sp/s10.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/187217865"
 },
 "Amanita rubescens": {
  "src": "img/sp/s11.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/187028349"
 },
 "Agaricus xanthodermus": {
  "src": "img/sp/s12.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/167651557"
 },
 "Morchella esculenta": {
  "src": "img/sp/s13.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/249501694"
 },
 "Armillaria mellea": {
  "src": "img/sp/s14.jpg",
  "atif": "(c) natomik, some rights reserved (CC BY)",
  "lisans": "cc-by",
  "kaynak": "https://www.inaturalist.org/observations/73316781"
 },
 "Agaricus campestris": {
  "src": "img/sp/s15.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/172876317"
 },
 "Boletus edulis": {
  "src": "img/sp/s16.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/245608179"
 },
 "Cantharellus cibarius": {
  "src": "img/sp/s17.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/241726630"
 },
 "Lactarius deliciosus": {
  "src": "img/sp/s18.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/139107306"
 },
 "Macrolepiota procera": {
  "src": "img/sp/s19.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/98191067"
 },
 "Amanita caesarea": {
  "src": "img/sp/s20.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/400695240"
 },
 "Hydnum repandum": {
  "src": "img/sp/s21.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/190829667"
 },
 "Craterellus cornucopioides": {
  "src": "img/sp/s22.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/311117480"
 },
 "Pleurotus ostreatus": {
  "src": "img/sp/s23.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/68431546"
 },
 "Coprinus comatus": {
  "src": "img/sp/s24.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/99856992"
 },
 "Marasmius oreades": {
  "src": "img/sp/s25.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/58984897"
 },
 "Ramaria spp.": {
  "src": "img/sp/s26.jpg",
  "atif": "no rights reserved",
  "lisans": "cc0",
  "kaynak": "https://www.inaturalist.org/observations/179124796"
 },
 "Grifola frondosa": {
  "src": "img/sp/s27.jpg",
  "atif": "(c) Lorenz Wenner, some rights reserved (CC BY)",
  "lisans": "cc-by",
  "kaynak": "https://www.inaturalist.org/observations/113253071"
 }
};
window.MYCO_REFS = {
 "genel": [
  {
   "ad": "White J. ve ark. Mushroom poisoning: A proposed new clinical classification. Toxicon 2019;157:53-65",
   "url": "https://doi.org/10.1016/j.toxicon.2018.11.007"
  },
  {
   "ad": "Diaz JH. Syndromic diagnosis and management of confirmed mushroom poisonings. Crit Care Med 2005;33(2):427-436",
   "url": "https://doi.org/10.1097/01.ccm.0000153531.69448.49"
  },
  {
   "ad": "T.C. Tarım ve Orman Bakanlığı (Ordu İl Müdürlüğü): Mantar zehirlenmeleri ve başlıca zehirli mantarlar",
   "url": "https://ordu.tarimorman.gov.tr/Belgeler/G%C4%B1da%20ve%20Yem/MANTAR%20ZEH%C4%B0RLENMELER%C4%B0%20VE%20BA%C5%9ELICA%20ZEH%C4%B0RL%C4%B0%20MANTARLAR.pdf"
  }
 ],
 "acil": {
  "ad": "114: Sağlık Bakanlığı Ulusal Zehir Danışma Merkezi (UZEM), 7/24 · 112: Acil Çağrı Merkezi",
  "url": "https://ordu.tarimorman.gov.tr/BelgelerArsiv/G%C4%B1da%20ve%20Yem/MANTAR%20ZEH%C4%B0RLENMELER%C4%B0NE%20D%C4%B0KKAT.pdf"
 },
 "turler": {
  "Amanita phalloides": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/52135"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5240325"
   }
  ],
  "Galerina marginata": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/1672638"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/8118872"
   }
  ],
  "Lepiota brunneoincarnata": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/515954"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2535390"
   }
  ],
  "Amanita muscaria": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48715"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/8168319"
   }
  ],
  "Amanita pantherina": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48418"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/8961574"
   }
  ],
  "Gyromitra esculenta": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/85120"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5258510"
   }
  ],
  "Omphalotus olearius": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/64021"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2538088"
   }
  ],
  "Entoloma sinuatum": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/510199"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2539308"
   }
  ],
  "Hypholoma fasciculare": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48767"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/3293632"
   }
  ],
  "Rubroboletus satanas": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/544554"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/7722553"
   }
  ],
  "Amanita rubescens": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/1678242"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/7496350"
   }
  ],
  "Agaricus xanthodermus": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/118394"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5243412"
   }
  ],
  "Morchella esculenta": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/58682"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2594602"
   }
  ],
  "Armillaria mellea": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/55950"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2536891"
   }
  ],
  "Agaricus campestris": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/143563"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5243458"
   }
  ],
  "Boletus edulis": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48701"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5954958"
   }
  ],
  "Cantharellus cibarius": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/47347"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5249504"
   }
  ],
  "Lactarius deliciosus": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/155197"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5248629"
   }
  ],
  "Macrolepiota procera": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/63401"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/8914748"
   }
  ],
  "Amanita caesarea": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/204588"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/5240269"
   }
  ],
  "Hydnum repandum": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48641"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2554716"
   }
  ],
  "Craterellus cornucopioides": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48607"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2554662"
   }
  ],
  "Pleurotus ostreatus": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/1196165"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2526530"
   }
  ],
  "Coprinus comatus": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/47392"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/7987658"
   }
  ],
  "Marasmius oreades": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/118240"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2537250"
   }
  ],
  "Ramaria spp.": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/48707"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2521461"
   }
  ],
  "Grifola frondosa": [
   {
    "ad": "iNaturalist tür sayfası",
    "url": "https://www.inaturalist.org/taxa/53714"
   },
   {
    "ad": "GBIF tür sayfası ve görülme kayıtları",
    "url": "https://www.gbif.org/species/2540800"
   }
  ]
 }
};
