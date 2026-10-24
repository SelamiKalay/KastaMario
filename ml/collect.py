"""1. adım — HAM veri toplama (bilerek temizlenmeden kaydedilir).

  * iNaturalist: species_info.csv'deki her tür için araştırma düzeyi, CC lisanslı
    gözlem fotoğrafları + 'mantar_degil' sınıfı için bitki/böcek fotoğrafları.
    -> data/raw/inat_photos.csv, data/raw/images/<photo_id>.jpg
  * GBIF: Türkiye'deki tüm mantar (Fungi) görülme kayıtları.
    -> data/raw/gbif_tr_fungi.csv

Yalnızca standart kütüphane kullanır. Yeniden çalıştırılabilir (inenleri atlar).

    python ml/collect.py            # hepsi
    python ml/collect.py --only gbif
"""
import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
IMG = RAW / "images"
UA = {"User-Agent": "MycoGuard-hackathon/0.2 (egitim projesi; mantar zehirlenme uyari prototipi)"}
INAT = "https://api.inaturalist.org/v1"
LICENSES = "cc0,cc-by,cc-by-nc,cc-by-sa,cc-by-nc-sa,cc-by-nd,cc-by-nc-nd"
OBS_PER_CLASS = 400       # sınıf başına en fazla gözlem
MIN_LOCAL_OBS = 200       # Avrupa+Türkiye'de bundan azsa dünya geneliyle tamamlanır
PHOTOS_PER_OBS = 2        # aynı gözlemin farklı açıları
# iNaturalist yer kimlikleri (places/autocomplete ile bulundu)
EUROPE, TURKEY = 97391, 7183
NEGATIVES = [("Plantae", 300), ("Pinaceae", 150), ("Bryophyta", 100), ("Insecta", 100)]

_last_call = [0.0]


def get_json(url, params=None, tries=4):
    """iNaturalist/GBIF API çağrısı; saniyede ~1 istek sınırına uyar."""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    for i in range(tries):
        wait = 1.1 - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - ağ hatalarında tekrar dene
            print(f"  ! {e} ({i + 1}/{tries})", flush=True)
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"İstek başarısız: {url}")


def taxon(name):
    """(taxon_id, iNaturalist'in kabul ettiği ad). Eş anlamlı adlar (sinonim) kabul edilen taksona çözülür."""
    name = name.removesuffix(" spp.")   # cins düzeyi sınıf: cinsin tüm türleri
    res = get_json(f"{INAT}/taxa", {"q": name, "per_page": 30})["results"]
    for t in res:
        if t["name"].lower() == name.lower():
            return t["id"], t["name"]
    for t in res:
        if (t.get("matched_term") or "").lower() == name.lower():
            print(f"  {name} -> iNaturalist kabul edilen ad: {t['name']}", flush=True)
            return t["id"], t["name"]
    raise RuntimeError(f"iNaturalist taksonu bulunamadı: {name}")


def observations(tid, place, limit):
    out, page = [], 1
    while len(out) < limit:
        params = {"taxon_id": tid, "quality_grade": "research", "photos": "true",
                  "photo_license": LICENSES, "per_page": 200, "page": page, "order_by": "votes"}
        if place:
            params["place_id"] = place
        res = get_json(f"{INAT}/observations", params)["results"]
        if not res:
            break
        out += res
        page += 1
    return out[:limit]


def photo_rows(sinif, tid, kabul_adi, obs, kapsam, per_obs):
    for o in obs:
        for ph in o.get("photos", [])[:per_obs]:
            yield {
                "photo_id": ph["id"], "observation_id": o["id"], "sinif": sinif, "istenen_taxon_id": tid,
                "istenen_taxon_adi": kabul_adi,
                "gozlem_taxon_adi": (o.get("taxon") or {}).get("name", ""),
                "gozlem_taxon_rank": (o.get("taxon") or {}).get("rank", ""),
                "lisans": ph.get("license_code") or "", "atif": ph.get("attribution", ""),
                "fotograf_url": (ph.get("url") or "").replace("/square.", "/medium."),
                "gozlem_tarihi": o.get("observed_on") or "", "konum": o.get("location") or "",
                "konum_dogrulugu_m": o.get("positional_accuracy") or "", "geoprivacy": o.get("geoprivacy") or "",
                "yer_metni": o.get("place_guess") or "", "kalite": o.get("quality_grade", ""), "kapsam": kapsam,
            }


def download(row):
    path = IMG / f'{row["photo_id"]}.jpg'
    if path.exists() or not row["fotograf_url"]:
        return
    for i in range(3):
        try:
            req = urllib.request.Request(row["fotograf_url"], headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                path.write_bytes(r.read())
            return
        except Exception:  # noqa: BLE001 - indirilemeyen dosya temizlikte elenir
            time.sleep(2 * (i + 1))


def collect_inat():
    IMG.mkdir(parents=True, exist_ok=True)
    with open(ROOT / "data" / "species_info.csv", encoding="utf-8") as f:
        species = [r["latin_name"] for r in csv.DictReader(f)]
    local, turkey = f"{EUROPE},{TURKEY}", TURKEY
    cache = RAW / "inat_cache"
    cache.mkdir(exist_ok=True)

    def sinif_topla(anahtar, fn):
        """Her sınıfın sonucu ayrı dosyaya yazılır: yarıda kesilirse kaldığı yerden devam eder."""
        f = cache / f"{anahtar.replace(' ', '_')}.json"
        if f.exists():
            return json.loads(f.read_text(encoding="utf-8")), True
        rows = fn()
        f.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        return rows, False

    def tur(name):
        tid, kabul = taxon(name)
        obs = observations(tid, local, OBS_PER_CLASS)
        kapsam = "avrupa_tr"
        if len(obs) < MIN_LOCAL_OBS:
            seen = {o["id"] for o in obs}
            extra = [o for o in observations(tid, None, OBS_PER_CLASS) if o["id"] not in seen]
            obs += extra[:OBS_PER_CLASS - len(obs)]
            kapsam = "avrupa_tr+dunya"
        return list(photo_rows(name, tid, kabul, obs, kapsam, PHOTOS_PER_OBS))

    def negatif(name, n):
        tid, kabul = taxon(name)
        return list(photo_rows("mantar_degil", tid, kabul, observations(tid, turkey, n), f"tr:{name}", 1))

    isler = [(n, lambda n=n: tur(n)) for n in species] + [(f"neg_{n}", lambda n=n, k=k: negatif(n, k)) for n, k in NEGATIVES]
    rows = []
    with ThreadPoolExecutor(8) as ex:
        for anahtar, fn in isler:
            yeni, onbellek = sinif_topla(anahtar, fn)
            rows += yeni
            list(ex.map(download, yeni))   # bu sınıfın fotoğraflarını hemen indir
            print(f"{anahtar:<32} {len(yeni):>4} foto {'(önbellekten)' if onbellek else ''}", flush=True)

    with open(RAW / "inat_photos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"\n{len(rows)} fotoğraf kaydı; diskte {sum(1 for _ in IMG.glob('*.jpg'))} dosya", flush=True)


GBIF_FIELDS = ["gbifID", "species", "scientificName", "taxonRank", "taxonKey", "speciesKey", "decimalLatitude",
               "decimalLongitude", "coordinateUncertaintyInMeters", "eventDate", "year", "month", "day",
               "stateProvince", "county", "locality", "basisOfRecord", "occurrenceStatus", "datasetName",
               "institutionCode", "recordedBy", "issues"]


GBIF = "https://api.gbif.org/v1"
KASTAMONU_BBOX = {"decimalLatitude": "40.85,42.05", "decimalLongitude": "32.55,34.95"}


def gbif_sorgulari():
    """Hedefli sorgular: rehberdeki her türün Türkiye kayıtları + Kastamonu çevresindeki tüm mantar kayıtları.
    Sorgular bilerek örtüşür; kopyalar temizlik adımında ayıklanır."""
    with open(ROOT / "data" / "species_info.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = get_json(f"{GBIF}/species/match", {"name": r["latin_name"].removesuffix(" spp."), "kingdom": "Fungi"}).get("usageKey")
            if key:
                yield f"tur:{r['latin_name']}", {"country": "TR", "taxonKey": key}
    yield "kastamonu:kutu", {"country": "TR", "kingdomKey": 5, **KASTAMONU_BBOX}
    yield "kastamonu:il", {"country": "TR", "kingdomKey": 5, "stateProvince": "Kastamonu"}


def collect_gbif():
    RAW.mkdir(parents=True, exist_ok=True)
    with open(RAW / "gbif_tr_fungi.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sorgu"] + GBIF_FIELDS, extrasaction="ignore")
        w.writeheader()
        for ad, q in gbif_sorgulari():
            offset, toplam = 0, None
            while toplam is None or offset < min(toplam, 100_000):  # arama API'sinin sayfalama sınırı
                sayfa = get_json(f"{GBIF}/occurrence/search", {**q, "limit": 300, "offset": offset}, tries=10)
                toplam = sayfa["count"]
                if not sayfa["results"]:
                    break
                for r in sayfa["results"]:
                    r["issues"] = ";".join(r.get("issues", []))
                    w.writerow({"sorgu": ad, **r})
                offset += len(sayfa["results"])
            print(f"GBIF {ad:<40} {toplam:>6} kayıt", flush=True)
    print("GBIF bitti.", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["inat", "gbif"])
    a = ap.parse_args()
    if a.only != "inat":
        collect_gbif()
    if a.only != "gbif":
        collect_inat()
