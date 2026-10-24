# Gemma 4'ün katkısı

Modelin eğitimde hiç görmediği **151 test fotoğrafı**, iki yoldan geçirildi: (A) yalnızca görüntü modeli + güvenlik kuralları, (B) A + Gemma 4 görsel özellik analizi. Gemma kuralı riski yalnızca yükseltebilir. Her fotoğraf tek açıdan çekilmiştir (uygulamada üç açı önerilir). Gemma hatası: 0.

| Metrik | Yalnızca model | Model + Gemma 4 |
|---|---:|---:|
| Zehirli/ölümcül tür → **KIRMIZI** (n=80) | 99% | **99%** |
| Zehirli/ölümcül tür → 'düşük riskli aday' (**tehlikeli karışıklık**) | 1% | **1%** |
| Düşük riskli tür → GRİ (gereksiz alarm olmaması, n=48) | 79% | 79% |
| Mantar olmayan fotoğraf reddedildi (n=8) | 88% | 88% |

- Gemma'nın KIRMIZI'ya çektiği zehirli tür fotoğrafı: **0**
- Amanita (köygöçüren, panter, sinek mantarı) fotoğraflarında Gemma'nın sap tabanında torba görme oranı: **8%** (n=24)
- Düşük riskli türlerde Gemma'nın riski KIRMIZI'ya çektiği oran (bedel): **0%**


Asimetrik maliyet: zehirliyi kaçırmak ölümcül olabilir; düşük riskli bir mantarda gereksiz alarm en fazla boş sepettir.
