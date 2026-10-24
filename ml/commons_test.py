"""Dış test seti: Wikimedia Commons'taki tür fotoğrafları (iNaturalist'ten bağımsız, 'internetten bulunan fotoğraf' benzeri).

Model iNaturalist'in orman fotoğraflarıyla eğitildi; gerçek kullanıcılar ise internetten, ekrandan ya da sepet/tezgâhtan
fotoğraf yükleyebiliyor. Bu set o dağılım kaymasını ölçmek içindir; eğitimde KULLANILMAZ.

Çıktı: data/raw/commons/<sinif>/<dosya>.jpg + data/raw/commons/liste.csv (lisans ve atıf ile)

    python ml/commons_test.py --tur 12
"""
import argparse
import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean import oku  # noqa: E402
from collect import get_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "raw" / "commons"
API = "https://commons.wikimedia.org/w/api.php"


def kategori_dosyalari(ad, n):
    """Commons 'Category:<Latince ad>' kategorisindeki fotoğraflar (500 px standart küçük resim + lisans)."""
    q = {"action": "query", "format": "json", "generator": "categorymembers", "gcmtitle": f"Category:{ad}",
         "gcmtype": "file", "gcmlimit": 50, "prop": "imageinfo", "iiprop": "url|extmetadata|mime", "iiurlwidth": 500}   # Wikimedia'nın standart küçük resim boyutlarından biri
    out = []
    for s in (get_json(API, q).get("query", {}).get("pages", {}) or {}).values():
        ii = (s.get("imageinfo") or [{}])[0]
        if ii.get("mime") != "image/jpeg" or not ii.get("thumburl"):
            continue
        meta = ii.get("extmetadata", {})
        out.append({"baslik": s["title"], "url": ii["thumburl"], "lisans": meta.get("LicenseShortName", {}).get("value", ""),
                    "yazar": meta.get("Artist", {}).get("value", "")[:120], "kaynak": ii.get("descriptionurl", "")})
    return out[:n]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--tur", type=int, default=12, help="tür başına en fazla fotoğraf")
    a = ap.parse_args()
    import urllib.error
    import urllib.request
    satirlar = []
    for r in oku(ROOT / "data" / "species_info.csv"):
        ad = r["latin_name"].removesuffix(" spp.")
        dizin = OUT / r["latin_name"].replace(" ", "_")
        dizin.mkdir(parents=True, exist_ok=True)
        for deneme in range(6):
            try:
                dosyalar = kategori_dosyalari(ad, a.tur)
                break
            except RuntimeError:
                time.sleep(30 * (deneme + 1))   # API hız sınırı
        time.sleep(4)
        for i, d in enumerate(dosyalar):
            hedef = dizin / f"{i:02d}.jpg"
            for deneme in range(5):
                if hedef.exists():
                    break
                try:
                    req = urllib.request.Request(d["url"], headers={"User-Agent": "KastaMario-hackathon/1.0 (egitim projesi)"})
                    hedef.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                except urllib.error.HTTPError as e:
                    if e.code != 429:
                        raise
                    time.sleep(20 * (deneme + 1))   # hız sınırı: bekle ve yeniden dene
                time.sleep(1.2)
            satirlar.append({"sinif": r["latin_name"], "dosya": str(hedef.relative_to(ROOT)), **d})
        print(f"{r['latin_name']:<30} {len(dosyalar)} fotoğraf", flush=True)
    with open(OUT / "liste.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(satirlar[0]))
        w.writeheader()
        w.writerows(satirlar)
    print(f"{len(satirlar)} fotoğraf -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
