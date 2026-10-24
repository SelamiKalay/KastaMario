"""Rehber için her türe bir temsilî fotoğraf seçer (CC lisanslı, atıflı).

Çıktı: app/img/sp/<id>.jpg (480x360) + data/clean/thumbs.json {latin_name: {src, atif, lisans, kaynak}}

    python ml/thumbs.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ml"))
from clean import ALLOWED_LICENSES, IMG, goruntu_kontrol, oku, tur_adi  # noqa: E402

OUT = ROOT / "app" / "img" / "sp"
# Tüm CC lisansları kabul; önce en serbest olanlar tercih edilir
TERCIH = ["cc0", "cc-by", "cc-by-sa", "cc-by-nc", "cc-by-nc-sa", "cc-by-nd", "cc-by-nc-nd"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    turler = {r["latin_name"]: r["id"] for r in oku(ROOT / "data" / "species_info.csv")}
    rows = []
    for r in oku(ROOT / "data" / "raw" / "inat_photos.csv"):
        lis = (r["lisans"] or "").lower()
        tur = tur_adi(r["gozlem_taxon_adi"])
        if lis in ALLOWED_LICENSES and tur and tur in (r["sinif"], tur_adi(r.get("istenen_taxon_adi"))):
            rows.append({**r, "lisans": lis})
    sonuc = {}
    for ad, sid in turler.items():
        adaylar = sorted((r for r in rows if r["sinif"] == ad), key=lambda r: TERCIH.index(r["lisans"]))[:40]
        for r in adaylar:
            p = IMG / f"{r['photo_id']}.jpg"
            ok, w, h, _ = goruntu_kontrol(p)
            if not ok or min(w, h) < 300:
                continue
            with Image.open(p) as im:
                ImageOps.fit(im.convert("RGB"), (480, 360), Image.Resampling.LANCZOS).save(OUT / f"{sid}.jpg", quality=82, optimize=True)
            sonuc[ad] = {"src": f"img/sp/{sid}.jpg", "atif": r["atif"], "lisans": r["lisans"],
                         "kaynak": f"https://www.inaturalist.org/observations/{r['observation_id']}"}
            break
        print(f"{ad:<30} {'✓' if ad in sonuc else '— uygun fotoğraf yok'}")
    (ROOT / "data" / "clean").mkdir(exist_ok=True)
    (ROOT / "data" / "clean" / "thumbs.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
