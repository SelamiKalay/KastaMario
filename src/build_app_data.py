"""data/ klasöründeki CSV ve JSON'u app/data.js'e gömer.

Böylece app/index.html internetsiz ve sunucusuz (çift tıklayarak) açılır.
Varsa data/clean/gbif_tur_istatistik.csv (ml/clean.py üretir) de eklenir.
Veriyi değiştirdikten sonra çalıştırın:

    python src/build_app_data.py
"""
import csv
import json

from decide import DATA, ROOT, load

cfg, info = load()
gbif = {}
stats = DATA / "clean" / "gbif_tur_istatistik.csv"
if stats.exists():
    with open(stats, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            gbif[r["latin_name"]] = {"tr": int(r["tr_kayit"]), "kastamonu": int(r["kastamonu_kayit"]),
                                     "aylar": [int(r[f"ay_{m:02d}"]) for m in range(1, 13)]}

thumbs_path = DATA / "clean" / "thumbs.json"
thumbs = json.loads(thumbs_path.read_text(encoding="utf-8")) if thumbs_path.exists() else {}
refs_path = DATA / "kaynaklar.json"
refs = json.loads(refs_path.read_text(encoding="utf-8")) if refs_path.exists() else {}

out = ROOT / "app" / "data.js"
dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1)  # noqa: E731
out.write_text(
    "// OTOMATİK ÜRETİLDİ: python src/build_app_data.py — elle düzenlemeyin.\n"
    f"window.MYCO_CASES = {dump(cfg)};\n"
    f"window.MYCO_SPECIES = {dump(list(info.values()))};\n"
    f"window.MYCO_GBIF = {dump(gbif)};\n"
    f"window.MYCO_THUMBS = {dump(thumbs)};\n"
    f"window.MYCO_REFS = {dump(refs)};\n",
    encoding="utf-8",
)
print(f"{out.relative_to(ROOT)} yazıldı ({len(info)} tür, {len(cfg['senaryolar'])} senaryo, "
      f"{len(gbif)} GBIF istatistiği, {len(thumbs)} tür fotoğrafı)")
