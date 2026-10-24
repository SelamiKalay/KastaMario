"""2. adım — VERİ TEMİZLEME ve AYRIŞTIRMA (veri madenciliği ön işleme).

Girdi : data/raw/inat_photos.csv, data/raw/images/, data/raw/gbif_tr_fungi.csv
Çıktı : data/clean/inat_clean.csv          (model eğitimi; split sütunu ile)
        data/clean/gbif_tr_clean.csv        (temiz Türkiye mantar kayıtları)
        data/clean/gbif_tur_istatistik.csv  (tür başına Türkiye/Kastamonu kayıt + ay dağılımı)
        data/clean/temizlik_raporu.md       (her adımda kaç kayıt elendi)

Yalnızca csv + numpy + Pillow kullanır (kayıtlar sözlük listesi olarak işlenir).

    python ml/clean.py
"""
import csv
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW, CLEAN = ROOT / "data" / "raw", ROOT / "data" / "clean"
IMG = RAW / "images"
SEED = 42

ALLOWED_LICENSES = {"cc0", "cc-by", "cc-by-nc", "cc-by-sa", "cc-by-nc-sa", "cc-by-nd", "cc-by-nc-nd"}
MIN_SIDE, MAX_ASPECT = 128, 3.0
NEAR_DUP_HAMMING = 4          # dHash farkı bu kadar veya azsa "aynı fotoğraf"
MAX_PER_CLASS, MIN_PER_CLASS = 450, 60
SPLIT = {"train": 0.70, "val": 0.15, "test": 0.15}
TR_BBOX = (35.8, 42.2, 25.6, 44.9)             # enlem min/max, boylam min/max
KASTAMONU_BBOX = (40.85, 42.05, 32.55, 34.95)  # yaklaşık; komşu illerin kenarlarını da kapsar


class Rapor:
    """Her temizlik adımında kayıt sayısını not eder."""

    def __init__(self):
        self.satirlar = []

    def adim(self, veri, ad, once, sonra, aciklama):
        self.satirlar.append((veri, ad, len(once), len(sonra), aciklama))
        print(f"  [{veri}] {ad:<34} {len(once):>7} -> {len(sonra):>7}", flush=True)
        return sonra

    def not_(self, veri, ad, n, aciklama):
        self.satirlar.append((veri, ad, n, n, aciklama))


def oku(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def yaz(path, rows, cols):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------ ortak ayrıştırıcılar
def tr_normalize(s):
    """'KASTAMONU İli', 'Kastamonu Province' -> 'kastamonu'."""
    if not isinstance(s, str):
        return ""
    s = s.replace("İ", "i").replace("I", "ı").lower().replace("ı", "i")
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = re.sub(r"\b(province|ili|il|vilayeti|prov\.?)\b", " ", s)
    kelimeler = re.sub(r"[^a-z ]", " ", s).split()
    return kelimeler[0] if kelimeler else ""


def tur_adi(ad):
    """Alt tür / varyete adını tür adına indirger: 'Amanita muscaria var. formosa' -> 'Amanita muscaria'."""
    if not isinstance(ad, str):
        return ""
    p = ad.split()
    return " ".join(p[:2]) if len(p) >= 2 and p[1][:1].islower() and p[1].isalpha() else ""


def tarih_ayristir(s):
    """'2021-10-03', '2021-10-03T14:00:00', '2021-10' -> (yıl, ay); geçersiz/gelecek -> (None, None)."""
    if not isinstance(s, str):
        return None, None
    m = re.match(r"^(\d{4})-(\d{1,2})", s.strip())
    if not m:
        return None, None
    y, mo = int(m.group(1)), int(m.group(2))
    if not (1800 <= y <= date.today().year and 1 <= mo <= 12):
        return None, None
    return y, mo


def konum_ayristir(s):
    """'41.37,33.77' -> (41.37, 33.77); geçersiz -> (None, None)."""
    try:
        lat, lon = (float(x) for x in str(s).split(","))
    except ValueError:
        return None, None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180) or (lat == 0 and lon == 0):
        return None, None
    return lat, lon


def sayi(s):
    try:
        v = float(s)
        return v if v == v else None
    except (TypeError, ValueError):
        return None


def in_bbox(lat, lon, b):
    return lat is not None and lon is not None and b[0] <= lat <= b[1] and b[2] <= lon <= b[3]


# ------------------------------------------------------------------ görüntü kontrolleri
def dhash(img, size=8):
    """Algısal fark hash'i (64 bit). Yeniden boyutlanmış/sıkıştırılmış kopyalar aynı veya çok yakın hash verir."""
    g = np.asarray(img.convert("L").resize((size + 1, size), Image.Resampling.LANCZOS), dtype=np.int16)
    bits = (g[:, 1:] > g[:, :-1]).flatten()
    return int(np.packbits(bits).view(">u8")[0])


def goruntu_kontrol(path):
    """(okunabilir_mi, genişlik, yükseklik, dhash)"""
    try:
        with Image.open(path) as im:
            im.load()
            return True, im.width, im.height, dhash(im)
    except Exception:  # noqa: BLE001 - bozuk / eksik dosya
        return False, 0, 0, None


def yakin_kopyalar(hashes, esik=NEAR_DUP_HAMMING, parca=2048):
    """Hamming uzaklığı <= esik olan çiftlerde sonradan gelenin indeksini döndürür (vektörel, parça parça)."""
    h = np.array(hashes, dtype=np.uint64)
    at = set()
    for i in range(0, len(h), parca):
        d = np.bitwise_count(h[i:i + parca, None] ^ h[None, :])
        for a, b in zip(*np.nonzero(d <= esik)):
            a = int(a) + i
            if b < a and int(b) not in at:
                at.add(a)
    return at


# ------------------------------------------------------------------ iNaturalist temizliği
def filtre_lisans(rows):
    out = []
    for r in rows:
        lis = (r.get("lisans") or "").strip().lower()
        if lis in ALLOWED_LICENSES:
            out.append({**r, "lisans": lis})
    return out


def rehberdekiler(rows, turler):
    """Rehberde (species_info.csv) olmayan sınıfları çıkarır; 'mantar_degil' korunur."""
    return [r for r in rows if r["sinif"] == "mantar_degil" or r["sinif"] in turler]


def taksonomi_normalize(rows):
    out = []
    for r in rows:
        tur = tur_adi(r["gozlem_taxon_adi"])
        # iNaturalist'in kabul ettiği ad, rehberdeki addan farklı olabilir (eş anlamlı / sinonim)
        if r["sinif"] == "mantar_degil" or (tur and tur in (r["sinif"], tur_adi(r.get("istenen_taxon_adi")))):
            out.append({**r, "tur": tur})
    return out


def ayir(rows, oranlar=SPLIT, seed=SEED):
    """Gözlem kimliğine göre katmanlı ayırma: bir gözlemin tüm fotoğrafları aynı tarafta kalır (sızıntı yok)."""
    rng = random.Random(seed)
    sinif_obs = defaultdict(set)
    for r in rows:
        sinif_obs[r["sinif"]].add(r["observation_id"])
    split = {}
    for s in sorted(sinif_obs):
        obs = sorted(sinif_obs[s])
        rng.shuffle(obs)
        n_tr = max(1, round(len(obs) * oranlar["train"]))
        n_va = max(1, round(len(obs) * oranlar["val"]))
        for i, o in enumerate(obs):
            split[o] = "train" if i < n_tr else "val" if i < n_tr + n_va else "test"
    return [{**r, "split": split[r["observation_id"]]} for r in rows]


def dengele(rows, en_fazla=MAX_PER_CLASS, en_az=MIN_PER_CLASS, seed=SEED):
    """Sınıf başına en fazla N fotoğraf (gözlem bütünlüğü korunarak); çok az örneği olan sınıflar çıkarılır."""
    rng = random.Random(seed)
    gruplar = defaultdict(lambda: defaultdict(list))
    for r in rows:
        gruplar[r["sinif"]][r["observation_id"]].append(r)
    out, atilan = [], []
    for s in sorted(gruplar):
        obs = gruplar[s]
        if sum(len(v) for v in obs.values()) < en_az:
            atilan.append(s)
            continue
        ids = sorted(obs)
        rng.shuffle(ids)
        toplam = 0
        for o in ids:
            if toplam + len(obs[o]) > en_fazla:
                break
            out += obs[o]
            toplam += len(obs[o])
    return out, atilan


def temizle_inat(rapor, turler):
    rows = oku(RAW / "inat_photos.csv")
    print(f"iNaturalist ham: {len(rows)} fotoğraf kaydı", flush=True)
    R = lambda ad, yeni, ack: rapor.adim("iNat", ad, rows, yeni, ack)  # noqa: E731

    gor = set()
    rows = R("1. Yinelenen photo_id", [r for r in rows if not (r["photo_id"] in gor or gor.add(r["photo_id"]))],
             "Aynı fotoğraf birden fazla sorguda gelmiş")
    rows = R("1b. Rehber dışı sınıflar", rehberdekiler(rows, set(turler)),
             "Kastamonu/Karadeniz'de GBIF kaydı olmadığı için rehberden çıkarılan türler")
    rows = R("2. Lisans filtresi", filtre_lisans(rows), "Yalnızca CC lisanslı fotoğraflar")
    rows = R("3. Eksik URL", [r for r in rows if r["fotograf_url"].startswith("http")], "Fotoğraf adresi olmayan kayıtlar")
    rows = R("4. Taksonomi normalizasyonu", taksonomi_normalize(rows), "Alt tür/varyete -> tür; sınıfla uyuşmayanlar atıldı")

    with ThreadPoolExecutor(8) as ex:
        kontrol = list(ex.map(goruntu_kontrol, [IMG / f"{r['photo_id']}.jpg" for r in rows]))
    for r, (ok, w, h, dh) in zip(rows, kontrol):
        r.update(okunur=ok, genislik=w, yukseklik=h, dhash=dh)
    rows = R("5. Bozuk / inmemiş görüntü", [r for r in rows if r["okunur"]], "Açılamayan veya indirilemeyen dosyalar")
    rows = R("6. Boyut / en-boy aykırı değer",
             [r for r in rows if min(r["genislik"], r["yukseklik"]) >= MIN_SIDE
              and max(r["genislik"], r["yukseklik"]) / max(1, min(r["genislik"], r["yukseklik"])) <= MAX_ASPECT],
             f"Kısa kenar < {MIN_SIDE}px veya en/boy > {MAX_ASPECT}")
    gor = set()
    rows = R("7. Birebir kopya (aynı dHash)", [r for r in rows if not (r["dhash"] in gor or gor.add(r["dhash"]))],
             "Farklı kimlikle yüklenmiş aynı fotoğraf")
    at = yakin_kopyalar([r["dhash"] for r in rows])
    rows = R("8. Neredeyse kopya (Hamming<=4)", [r for i, r in enumerate(rows) if i not in at],
             "Kırpılmış/sıkıştırılmış kopyalar (train-test sızıntısını önler)")

    for r in rows:
        r["yil"], r["ay"] = tarih_ayristir(r["gozlem_tarihi"])
        r["enlem"], r["boylam"] = konum_ayristir(r["konum"])
        r["turkiye"] = in_bbox(r["enlem"], r["boylam"], TR_BBOX)
    rapor.not_("iNat", "9. Tarih / konum ayrıştırma", len(rows),
               f"Ay bilinmeyen: {sum(r['ay'] is None for r in rows)}, konum bilinmeyen: {sum(r['enlem'] is None for r in rows)} (atılmadı)")

    once = rows
    rows, atilan = dengele(rows)
    rapor.adim("iNat", "10. Sınıf dengeleme", once, rows,
               f"Sınıf başına en fazla {MAX_PER_CLASS}; < {MIN_PER_CLASS} örnekli sınıflar çıkarıldı: {', '.join(atilan) or 'yok'}")
    rows = ayir(rows)
    yaz(CLEAN / "inat_clean.csv", rows, ["photo_id", "observation_id", "sinif", "tur", "lisans", "atif", "genislik", "yukseklik",
                                          "dhash", "yil", "ay", "enlem", "boylam", "turkiye", "kapsam", "split"])
    return rows, atilan


# ------------------------------------------------------------------ GBIF temizliği
def temizle_gbif(rapor, turler):
    rows = oku(RAW / "gbif_tr_fungi.csv")
    print(f"GBIF ham: {len(rows)} kayıt", flush=True)
    R = lambda ad, yeni, ack: rapor.adim("GBIF", ad, rows, yeni, ack)  # noqa: E731

    gor = set()
    rows = R("1. Yinelenen gbifID", [r for r in rows if not (r["gbifID"] in gor or gor.add(r["gbifID"]))], "Aynı kayıt birden çok sayfada")
    rows = R("2. 'Yok' (ABSENT) kayıtlar", [r for r in rows if r["occurrenceStatus"].upper() != "ABSENT"], "Türün bulunmadığını bildiren kayıtlar")
    for r in rows:
        r["tur"] = tur_adi(r["species"].strip() or r["scientificName"])
    rows = R("3. Tür düzeyine indirgeme", [r for r in rows if r["tur"]], "Cins veya üstü düzeyde tanımlanan kayıtlar")
    for r in rows:
        r["enlem"], r["boylam"] = sayi(r["decimalLatitude"]), sayi(r["decimalLongitude"])
    sorun = re.compile(r"ZERO_COORDINATE|COUNTRY_COORDINATE_MISMATCH|PRESUMED_SWAPPED")
    rows = R("4. Koordinat aykırı değerleri",
             [r for r in rows if not sorun.search(r["issues"]) and (r["enlem"] is None or in_bbox(r["enlem"], r["boylam"], TR_BBOX))],
             "Türkiye dışı, 0/0 veya ters girilmiş koordinatlar")
    for r in rows:
        ay = sayi(r["month"])
        r["ay"] = int(ay) if ay and 1 <= ay <= 12 else tarih_ayristir(r["eventDate"])[1]
    gor = set()
    anahtar = lambda r: (r["tur"], round(r["enlem"], 3) if r["enlem"] is not None else None,  # noqa: E731
                         round(r["boylam"], 3) if r["boylam"] is not None else None, r["eventDate"][:10])
    rows = R("5. Aynı tür-yer-gün kopyaları", [r for r in rows if not (anahtar(r) in gor or gor.add(anahtar(r)))],
             "Aynı gözlemin farklı veri setlerindeki kopyası")
    yazimlar = Counter(r["stateProvince"] for r in rows if r["stateProvince"])
    for r in rows:
        r["il_norm"] = tr_normalize(r["stateProvince"])
        r["kastamonu"] = r["il_norm"] == "kastamonu" or (r["il_norm"] == "" and in_bbox(r["enlem"], r["boylam"], KASTAMONU_BBOX))
    kast_yazim = sorted(y for y in yazimlar if tr_normalize(y) == "kastamonu")
    rapor.not_("GBIF", "6. İl adı normalizasyonu", len(rows),
               f"{len(yazimlar)} farklı yazım -> {len({tr_normalize(y) for y in yazimlar})} il; Kastamonu yazımları: "
               f"{', '.join(repr(y) for y in kast_yazim) or '—'}; Kastamonu kaydı: {sum(r['kastamonu'] for r in rows)}")
    yaz(CLEAN / "gbif_tr_clean.csv", rows, ["gbifID", "tur", "enlem", "boylam", "ay", "eventDate", "il_norm", "kastamonu",
                                             "basisOfRecord", "datasetName"])
    tur_rows = defaultdict(list)
    for r in rows:
        tur_rows[r["tur"]].append(r)
    with open(CLEAN / "gbif_tur_istatistik.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["latin_name", "tr_kayit", "kastamonu_kayit"] + [f"ay_{m:02d}" for m in range(1, 13)])
        for t in turler:
            g = tur_rows.get(t, [])
            aylar = Counter(r["ay"] for r in g if r["ay"])
            w.writerow([t, len(g), sum(r["kastamonu"] for r in g)] + [aylar.get(m, 0) for m in range(1, 13)])
    return rows


# ------------------------------------------------------------------ rapor
def rapor_yaz(rapor, inat, atilan, gbif, turler):
    L = ["# Veri temizleme raporu", "", f"Üretim: `python ml/clean.py` — tohum (seed) {SEED}", "",
         "## Adım adım", "", "| Veri | Adım | Önce | Sonra | Elenen | Açıklama |", "|---|---|---:|---:|---:|---|"]
    L += [f"| {v} | {a} | {o} | {s} | {o - s} | {ack} |" for v, a, o, s, ack in rapor.satirlar]
    if inat is not None:
        L += ["", "## Model veri seti (sınıf × ayrım)", "", "| Sınıf | train | val | test | toplam | gözlem |", "|---|---:|---:|---:|---:|---:|"]
        sinif = defaultdict(list)
        for r in inat:
            sinif[r["sinif"]].append(r)
        for s in sorted(sinif):
            c = Counter(r["split"] for r in sinif[s])
            L.append(f"| {s} | {c['train']} | {c['val']} | {c['test']} | {len(sinif[s])} | {len({r['observation_id'] for r in sinif[s]})} |")
        obs_split = defaultdict(set)
        for r in inat:
            obs_split[r["observation_id"]].add(r["split"])
        L += ["", f"Çıkarılan sınıflar (< {MIN_PER_CLASS} örnek): {', '.join(atilan) or 'yok'}",
              f"Türkiye'den gelen fotoğraf: {sum(r['turkiye'] for r in inat)} / {len(inat)}", "",
              "Sızıntı kontrolü (her gözlem yalnızca bir ayrımda): " + ("✅ geçti" if max(map(len, obs_split.values())) == 1 else "❌")]
    if gbif is not None:
        tur_say = Counter(r["tur"] for r in gbif)
        kast = Counter(r["tur"] for r in gbif if r["kastamonu"])
        L += ["", "## GBIF — rehberdeki türler", "", "| Tür | Türkiye | Kastamonu |", "|---|---:|---:|"]
        L += [f"| *{t}* | {tur_say[t]} | {kast[t]} |" for t in turler]
        L += ["", f"## Kastamonu'da en çok kaydı olan 25 tür (GBIF, toplam {sum(kast.values())} kayıt)", "",
              "| Tür | Kayıt | Rehberde |", "|---|---:|:---:|"]
        L += [f"| *{t}* | {n} | {'✅' if t in turler else ''} |" for t, n in kast.most_common(25)]
    (CLEAN / "temizlik_raporu.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    CLEAN.mkdir(parents=True, exist_ok=True)
    turler = [r["latin_name"] for r in oku(ROOT / "data" / "species_info.csv")]
    rapor = Rapor()
    gbif = temizle_gbif(rapor, turler) if (RAW / "gbif_tr_fungi.csv").exists() else None
    inat, atilan = temizle_inat(rapor, turler) if (RAW / "inat_photos.csv").exists() else (None, [])
    rapor_yaz(rapor, inat, atilan, gbif, turler)
    print(f"\nRapor: {(CLEAN / 'temizlik_raporu.md').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
