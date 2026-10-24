# Güvenlik ve etik ilkeleri

## Temel ilke: asimetrik maliyet
Zehirliyi yenilebilir sanmak ölümcül olabilir; yenilebiliri zehirli sanmak en fazla boş sepet demektir. Bu yüzden sistem her zaman **en kötü adayı** esas alır.

## Kurallar
1. **Uygulama asla "bu mantar yenilebilir / güvenli" demez.** Kod ve arayüzde "güvenli" etiketi yoktur.
2. **Yeşil renk kullanılmaz.** Seviyeler: kırmızı, sarı, gri, mor (mantar değil).
3. **Tek tahmin gösterilmez.** Her zaman ilk 5 aday ve olasılıkları gösterilir.
4. **En kötü aday kuralı:** Adaylardan herhangi biri ≥%5 olasılıkla ölümcül/yüksek riskliyse sonuç KIRMIZI'dır — birinci tahmin ne olursa olsun.
5. **Emin değilken tahmin edilmez:** Birinci aday <%60 ise SARI; kullanıcıdan yeni fotoğraf (sap tabanı dahil) istenir.
6. **Mantar olmayan girdi reddedilir;** kozalağa "tür" uydurulmaz.
7. **Zehirlilik bilgisi modelden çıkarılmaz,** her zaman uzman onaylı bilgi tabanından gelir.
8. Her ekranda **sabit uyarı bandı** ve **acil durum butonu** bulunur.
9. Prototipte her ekranda **"SİMÜLE DEMO"** rozeti bulunur; demo gerçek model sanılmamalıdır.

## Bilerek yapmadıklarımız
- Pişirme / yeme önerisi
- "Güvenli" etiketi
- Tek fotoğrafa tam güven

## Veri ve gizlilik
- Kullanıcı fotoğrafları ve konumları prototipte toplanmaz.
- Gerçek üründe vaka istatistikleri yalnızca **anonim ve toplu** biçimde kullanılır.

## Hukuki
Uygulama bir uzman veya hekim yerine geçmez. Sorumluluk reddi README'de ve arayüzde yer alır. Acil durum numaraları resmî kaynaklardan doğrulanmadan sunuma çıkılmaz.
