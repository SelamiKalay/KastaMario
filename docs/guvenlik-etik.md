# Güvenlik ve etik ilkeleri

## Temel ilke: asimetrik maliyet
Zehirliyi yenilebilir sanmak ölümcül olabilir; yenilebiliri zehirli sanmak en fazla boş sepet demektir. Bu yüzden sistem her zaman **en kötü adayı** esas alır.

## Kurallar
1. **Uygulama asla "bu mantar yenilebilir / güvenli" demez.** Arayüzde ve bilgi tabanında bu ifadeler yoktur (`tests/test_species_table.py` denetler).
2. **Yeşil renk kullanılmaz.** Seviyeler: kırmızı, sarı, gri, mor (mantar değil).
3. **Tek tahmin gösterilmez.** Her zaman en olası 5 tür ve olasılıkları gösterilir.
4. **En kötü aday kuralı:** Adaylardan herhangi biri ≥%5 olasılıkla ölümcül/zehirliyse sonuç KIRMIZI'dır — birinci tahmin ne olursa olsun.
5. **Emin değilken tahmin edilmez:** Birinci aday <%60 ise SARI; kullanıcıdan eksik açılardan (sap tabanı dahil) yeni fotoğraf istenir.
6. **Mantar olmayan girdi reddedilir;** kozalağa "tür" uydurulmaz.
7. **Zehirlilik bilgisi modelden çıkarılmaz,** her zaman bilgi tabanından gelir.
8. Her ekranda **acil durum** erişimi (Yedim! sekmesi, 114 / 112) bulunur.

## Gemma 4 için ek kurallar
9. **Yapılandırılmış çıktı:** Gemma'dan serbest "yenir/yenmez" yorumu istenmez; yalnızca görünen özellikler JSON şemasıyla istenir (`temperature: 0`). Emin olmadığı her şey için "görünmüyor" yazması istenir.
10. **Yalnızca yükseltme:** Gemma bulguları riski yükseltebilir (torba → KIRMIZI, kötü fotoğraf → SARI), **asla düşüremez** (`app/decide.js: escalate`, `tests/test_gemma.py`).
11. **Bilgi tabanına dayalı yanıt (RAG):** Asistan yalnızca `species_info.csv`'deki ilgili türlerin bilgisiyle yanıt verir; yanıtlar yasak ifade süzgecinden geçer.
12. **Acil durum önceliği:** Kullanıcı mantar yediğini söylerse asistan önce 112 / 114'ü önerir.
13. **Gizlilik:** Gemma yerel çalışır (Ollama); fotoğraflar üçüncü taraf bir buluta gönderilmez.

## Bilerek yapmadıklarımız
- Pişirme / yeme önerisi
- "Güvenli" etiketi
- Tek fotoğrafa tam güven

## Ölçülen güvenlik metrikleri
`results/egitim_raporu.md`: zehirli tür fotoğrafının KIRMIZI gösterilme oranı ve **tehlikeli karışıklık oranı** (zehirli → "düşük riskli aday"; hedef ≈ 0).

## Hukuki
Uygulama bir uzman veya hekim yerine geçmez. Sorumluluk reddi README'de ve arayüzde yer alır.
