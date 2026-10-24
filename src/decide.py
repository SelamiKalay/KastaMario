"""MycoGuard karar katmanı.

Model çıktısı (simüle top-5) + tür bilgi tablosu -> risk seviyesi.
Bağımlılık yok; çalıştırınca 8 demo senaryosunu test eder:

    python src/decide.py
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load():
    cfg = json.loads((DATA / "demo_cases.json").read_text(encoding="utf-8"))
    with open(DATA / "species_info.csv", encoding="utf-8", newline="") as f:
        info = {r["latin_name"]: r for r in csv.DictReader(f)}
    return cfg, info


def decide(case, info, T):
    """En kötü aday kuralı: tehlikeli bir aday yeterli olasılıktaysa sonuç KIRMIZI."""
    if case["mantar_olma_olasiligi"] < T["mantar_degil_esigi"]:
        return "MANTAR_DEGIL"
    top5 = case["simule_top5"]
    tehlikeli = [x for x in top5
                 if x["p"] >= T["tehlikeli_aday_min_olasilik"]
                 and info[x["latin_name"]]["risk"] in T["tehlikeli_risk_seviyeleri"]]
    if tehlikeli:
        return "KIRMIZI"
    top1 = top5[0]
    if top1["p"] < T["belirsizlik_esigi"] or info[top1["latin_name"]]["risk"] == "orta":
        return "SARI"
    return "GRI"


def escalate(level, g):
    """Gemma 4 görsel bulguları riski yalnızca YÜKSELTİR (app/decide.js escalate ile aynı kural).
    g: /api/analiz yanıtı {ozellikler, kirmiziya_cek, uyarilar} ya da None."""
    if not g or not g.get("ozellikler"):
        return level
    oz = g["ozellikler"]
    if level == "MANTAR_DEGIL":
        return ("KIRMIZI" if g.get("kirmiziya_cek") else "SARI") if oz.get("mantar_mi") else level
    if g.get("kirmiziya_cek"):
        return "KIRMIZI"
    if oz.get("foto_kalitesi") == "kotu" and level == "GRI":
        return "SARI"
    return level


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cfg, info = load()
    T = cfg["esikler"]
    hata = 0
    for c in cfg["senaryolar"]:
        eksik = [x["latin_name"] for x in c["simule_top5"] if x["latin_name"] not in info]
        if eksik:
            print(c["id"], "HATA: tabloda olmayan tür", eksik)
            hata += 1
            continue
        sonuc = decide(c, info, T)
        ok = sonuc == c["beklenen_seviye"]
        hata += not ok
        print(f'{c["id"]:<3} {sonuc:<13} {"OK" if ok else "HATA (beklenen " + c["beklenen_seviye"] + ")"}')
    print(f"\n{len(cfg['senaryolar']) - hata}/{len(cfg['senaryolar'])} senaryo OK")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
