# data/

| Dosya | İçerik |
|---|---|
| `species_info.csv` | 20 türlük demo bilgi tablosu. **Tüm satırlar TASLAK**, kaynakla doğrulanacak. `dusuk` risk "güvenli" demek değildir. |
| `demo_cases.json` | Karar eşikleri + 8 senaryo. `simule_top5` değerleri **elle verilmiştir**, gerçek modelden gelmez. |

Değişiklikten sonra: `python src/decide.py` (test) ve `python src/build_app_data.py` (arayüz verisi).

## Gerçek görüntü verisi (repoya konmaz)
Görüntü veri setleri büyük olduğu ve lisansları farklı olduğu için repoya eklenmez. İndirme:

```bash
pip install kaggle
kaggle datasets download -d picekl/fungitastic          # FungiTastic (önce Mini alt kümesini seçin)
kaggle datasets download -d thehir0/mushroom-species    # yardımcı veri, lisansı doğrulanmadı
```

İndirilen veriyi `data/raw/` altına koyun (`.gitignore` ile hariç tutulur). Kaynaklar ve lisanslar: `docs/veri-kaynaklari.md`.
