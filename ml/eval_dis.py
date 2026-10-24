"""Dış test: Wikimedia Commons fotoğrafları (internetten bulunan fotoğraf benzeri) + iNaturalist test seti.
Tek bakış (orta kare) ile çoklu bakış (orta + tam + ayna, uygulamadaki yöntem) karşılaştırılır.

    python ml/eval_dis.py
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent / "src")]
from decide import decide, load  # noqa: E402
from eval_gemma import IMG, ROOT, Model  # noqa: E402

TEHLIKELI = {"olumcul", "yuksek"}


def olc(model, ornekler, info, T, bakislar):
    s = defaultdict(int)
    tur = defaultdict(lambda: [0, 0])
    for sinif, yol in ornekler:
        v = model.vaka(yol, bakislar)
        adlar = [x["latin_name"] for x in v["simule_top5"]]
        karar = decide(v, info, T)
        s["n"] += 1
        s["top1"] += adlar[0] == sinif
        s["top5"] += sinif in adlar
        tur[sinif][0] += adlar[0] == sinif
        tur[sinif][1] += 1
        if info[sinif]["risk"] in TEHLIKELI:
            s["teh_n"] += 1
            s["teh_kirmizi"] += karar == "KIRMIZI"
            s["teh_gri"] += karar == "GRI"
    return {"n": s["n"], "top1": s["top1"] / s["n"], "top5": s["top5"] / s["n"],
            "tehlikeli_kirmizi": s["teh_kirmizi"] / max(1, s["teh_n"]), "tehlikeli_gri": s["teh_gri"] / max(1, s["teh_n"]),
            "tur_top1": {k: a / b for k, (a, b) in tur.items()}}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cfg, info = load()
    T = cfg["esikler"]
    model = Model(sys.argv[1]) if len(sys.argv) > 1 else Model()   # isteğe bağlı: karşılaştırma için başka model klasörü
    siniflar = set(model.meta["classes"])
    commons = [(r["sinif"], ROOT / r["dosya"]) for r in csv.DictReader(open(ROOT / "data/raw/commons/liste.csv", encoding="utf-8"))
               if r["sinif"] in siniflar and (ROOT / r["dosya"]).exists()]
    inat = [(r["sinif"], IMG / f"{r['photo_id']}.jpg") for r in csv.DictReader(open(ROOT / "data/clean/inat_clean.csv", encoding="utf-8"))
            if r["split"] == "test" and r["sinif"] != "mantar_degil"]
    sonuc = {}
    for ad, ornek in [("commons", commons), ("inat_test", inat)]:
        for bakis_ad, bakislar in [("tek", ("orta",)), ("coklu", ("orta", "tam", "ayna"))]:
            r = olc(model, ornek, info, T, bakislar)
            sonuc[f"{ad}_{bakis_ad}"] = r
            print(f"{ad:<10} {bakis_ad:<6} n={r['n']:<5} top1 {r['top1']:.1%}  top5 {r['top5']:.1%}  "
                  f"tehlikeli→KIRMIZI {r['tehlikeli_kirmizi']:.1%}  tehlikeli→GRİ {r['tehlikeli_gri']:.1%}", flush=True)
    kotu = sorted(sonuc["commons_coklu"]["tur_top1"].items(), key=lambda x: x[1])[:6]
    print("Commons'ta en zayıf türler (çoklu bakış top-1):", ", ".join(f"{k} {v:.0%}" for k, v in kotu))
    (ROOT / "results" / "dis_test.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
