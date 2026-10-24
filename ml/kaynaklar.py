"""Tür sayfaları için kaynak bağlantıları: iNaturalist ve GBIF tür sayfaları + genel klinik kaynaklar.

Çıktı: data/kaynaklar.json   (src/build_app_data.py uygulamaya gömer)

    python ml/kaynaklar.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean import oku  # noqa: E402
from collect import GBIF, get_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Bilgi tabanındaki zehirlenme sendromları, belirti süreleri ve ilk yardım adımları için genel kaynaklar
GENEL = [
    {"ad": "White J. ve ark. Mushroom poisoning: A proposed new clinical classification. Toxicon 2019;157:53-65",
     "url": "https://doi.org/10.1016/j.toxicon.2018.11.007"},
    {"ad": "Diaz JH. Syndromic diagnosis and management of confirmed mushroom poisonings. Crit Care Med 2005;33(2):427-436",
     "url": "https://doi.org/10.1097/01.ccm.0000153531.69448.49"},
    {"ad": "T.C. Tarım ve Orman Bakanlığı (Ordu İl Müdürlüğü): Mantar zehirlenmeleri ve başlıca zehirli mantarlar",
     "url": "https://ordu.tarimorman.gov.tr/Belgeler/G%C4%B1da%20ve%20Yem/MANTAR%20ZEH%C4%B0RLENMELER%C4%B0%20VE%20BA%C5%9ELICA%20ZEH%C4%B0RL%C4%B0%20MANTARLAR.pdf"},
]
ACIL = {"ad": "114: Sağlık Bakanlığı Ulusal Zehir Danışma Merkezi (UZEM), 7/24 · 112: Acil Çağrı Merkezi",
        "url": "https://ordu.tarimorman.gov.tr/BelgelerArsiv/G%C4%B1da%20ve%20Yem/MANTAR%20ZEH%C4%B0RLENMELER%C4%B0NE%20D%C4%B0KKAT.pdf"}


def inat_kimlikleri():
    out = {}
    for f in (ROOT / "data" / "raw" / "inat_cache").glob("*.json"):
        rows = json.loads(f.read_text(encoding="utf-8"))
        if rows and rows[0]["sinif"] != "mantar_degil":
            out[rows[0]["sinif"]] = rows[0]["istenen_taxon_id"]
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    inat = inat_kimlikleri()
    turler = {}
    for r in oku(ROOT / "data" / "species_info.csv"):
        ad = r["latin_name"]
        key = get_json(f"{GBIF}/species/match", {"name": ad.removesuffix(" spp."), "kingdom": "Fungi"}).get("usageKey")
        turler[ad] = [x for x in [
            {"ad": "iNaturalist tür sayfası", "url": f"https://www.inaturalist.org/taxa/{inat[ad]}"} if ad in inat else None,
            {"ad": "GBIF tür sayfası ve görülme kayıtları", "url": f"https://www.gbif.org/species/{key}"} if key else None,
        ] if x]
        print(f"{ad:<30} {len(turler[ad])} bağlantı")
    out = ROOT / "data" / "kaynaklar.json"
    out.write_text(json.dumps({"genel": GENEL, "acil": ACIL, "turler": turler}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{out.relative_to(ROOT)} yazıldı")


if __name__ == "__main__":
    main()
