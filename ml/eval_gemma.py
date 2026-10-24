"""4. adım — GEMMA 4'ÜN KATKISI: aynı test fotoğrafları iki yoldan geçirilir ve karşılaştırılır.

  A) Görüntü modeli (ONNX, uygulamadaki ile aynı ön işleme) + güvenlik kuralları
  B) A + Gemma 4 görsel özellikleri (riski yalnızca yükseltir)

Girdi : data/clean/inat_clean.csv (yalnızca test ayrımı), app/model/, Gemini API (.env)
Çıktı : results/gemma_degerlendirme.md, results/gemma_degerlendirme.json
        results/gemma_onbellek.json  (Gemma yanıtları; yeniden çalıştırınca API çağrılmaz)

    python ml/eval_gemma.py                # varsayılan örneklem
    python ml/eval_gemma.py --tehlikeli 12 # tehlikeli tür başına daha çok fotoğraf
"""
import argparse
import base64
import io
import json
import random
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "server"), str(ROOT / "ml")]
import app as _sunucu  # noqa: E402,F401  (.env içindeki API anahtarını yükler)
import gemma  # noqa: E402
from clean import oku  # noqa: E402
from decide import decide, escalate, load  # noqa: E402

IMG = ROOT / "data" / "raw" / "images"
RES = ROOT / "results"
ONBELLEK = RES / "gemma_onbellek.json"
TEHLIKELI = {"olumcul", "yuksek"}
AMANITA = {"Amanita phalloides", "Amanita pantherina", "Amanita muscaria"}


class Model:
    """app/model.js ile aynı: kısa kenar -> input_size, ortadan kırp, normalize, sıcaklıkla softmax."""

    def __init__(self):
        self.meta = json.loads((ROOT / "app" / "model" / "labels.json").read_text(encoding="utf-8"))
        self.sess = ort.InferenceSession(str(ROOT / "app" / "model" / "mycoguard.onnx"))

    def vaka(self, path):
        m, S = self.meta, self.meta["input_size"]
        with Image.open(path) as im:
            im = im.convert("RGB")
            k = S / min(im.size)
            im = im.resize((max(S, round(im.width * k)), max(S, round(im.height * k))), Image.Resampling.BILINEAR)
            l, t = (im.width - S) // 2, (im.height - S) // 2
            x = (np.asarray(im.crop((l, t, l + S, t + S)), dtype=np.float32) / 255 - m["mean"]) / m["std"]
        logit = self.sess.run(None, {"input": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0] / m.get("temperature", 1)
        p = np.exp(logit - logit.max())
        p /= p.sum()
        cls = m["classes"]
        neg = cls.index("mantar_degil") if "mantar_degil" in cls else -1
        p_not = float(p[neg]) if neg >= 0 else 0.0
        tur = sorted(((c, float(p[i]) / max(1e-9, 1 - p_not)) for i, c in enumerate(cls) if i != neg), key=lambda x: -x[1])
        return {"mantar_olma_olasiligi": 1 - p_not, "simule_top5": [{"latin_name": c, "p": q} for c, q in tur[:5]]}


def b64(path, mx=640):
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail((mx, mx))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def gemma_analiz(path, deneme=6):
    """Hız sınırına (429) takılırsa bekleyip yeniden dener."""
    for i in range(deneme):
        try:
            oz = gemma.gorsel_ozellikler([b64(path)])
            return {"ozellikler": oz, **gemma.risk_yukseltme(oz)}
        except gemma.LLMHatasi as e:
            if i == deneme - 1:
                return {"hata": str(e)[:200]}
            time.sleep(15 * (i + 1) if "429" in str(e) else 5)


def ornekle(rows, info, a):
    rng = random.Random(42)
    sinif = defaultdict(list)
    for r in rows:
        if r["split"] == "test":
            sinif[r["sinif"]].append(r)
    secim = []
    for s, g in sorted(sinif.items()):
        risk = "mantar_degil" if s == "mantar_degil" else info[s]["risk"]
        n = a.tehlikeli if risk in TEHLIKELI else a.orta if risk == "orta" else a.dusuk if risk == "dusuk" else a.negatif
        rng.shuffle(g)
        secim += [{**r, "risk": risk} for r in g[:n]]
    return secim


def oran(liste, kosul):
    return sum(map(kosul, liste)) / len(liste) if liste else None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--tehlikeli", type=int, default=8)
    ap.add_argument("--orta", type=int, default=3)
    ap.add_argument("--dusuk", type=int, default=4)
    ap.add_argument("--negatif", type=int, default=8)
    ap.add_argument("--paralel", type=int, default=3)
    a = ap.parse_args()
    if not gemma.durum()["hazir"]:
        sys.exit("Gemma hazır değil: .env içinde GEMINI_API_KEY tanımlayın.")
    cfg, info = load()
    T = cfg["esikler"]
    model = Model()
    secim = ornekle(oku(ROOT / "data" / "clean" / "inat_clean.csv"), info, a)
    onbellek = json.loads(ONBELLEK.read_text(encoding="utf-8")) if ONBELLEK.exists() else {}
    eksik = [r for r in secim if r["photo_id"] not in onbellek]
    print(f"{len(secim)} test fotoğrafı; Gemma'ya gidecek: {len(eksik)} (önbellekte {len(secim) - len(eksik)})", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(a.paralel) as ex:
        for i, (r, g) in enumerate(zip(eksik, ex.map(lambda r: gemma_analiz(IMG / f"{r['photo_id']}.jpg"), eksik)), 1):
            onbellek[r["photo_id"]] = g
            if i % 10 == 0 or i == len(eksik):
                ONBELLEK.write_text(json.dumps(onbellek, ensure_ascii=False), encoding="utf-8")
                print(f"  {i}/{len(eksik)}  ({time.time() - t0:.0f} sn)", flush=True)

    sonuc = []
    for r in secim:
        vaka = model.vaka(IMG / f"{r['photo_id']}.jpg")
        once = decide(vaka, info, T)
        g = onbellek[r["photo_id"]]
        sonra = escalate(once, None if "hata" in g else g)
        sonuc.append({"photo_id": r["photo_id"], "observation_id": r["observation_id"], "sinif": r["sinif"], "risk": r["risk"],
                      "model_ilk": vaka["simule_top5"][0]["latin_name"], "once": once, "sonra": sonra,
                      "gemma_hata": "hata" in g, "kirmiziya_cek": bool(g.get("kirmiziya_cek")),
                      "torba": g.get("ozellikler", {}).get("sap_tabaninda_torba")})

    tehlikeli = [x for x in sonuc if x["risk"] in TEHLIKELI]
    dusuk = [x for x in sonuc if x["risk"] == "dusuk"]
    negatif = [x for x in sonuc if x["risk"] == "mantar_degil"]
    amanita = [x for x in sonuc if x["sinif"] in AMANITA]
    m = {
        "foto_sayisi": len(sonuc), "gemma_hata": sum(x["gemma_hata"] for x in sonuc),
        "tehlikeli_n": len(tehlikeli),
        "tehlikeli_kirmizi_once": oran(tehlikeli, lambda x: x["once"] == "KIRMIZI"),
        "tehlikeli_kirmizi_sonra": oran(tehlikeli, lambda x: x["sonra"] == "KIRMIZI"),
        "tehlikeli_gri_once": oran(tehlikeli, lambda x: x["once"] == "GRI"),
        "tehlikeli_gri_sonra": oran(tehlikeli, lambda x: x["sonra"] == "GRI"),
        "tehlikeli_kurtarilan": sum(x["once"] != "KIRMIZI" and x["sonra"] == "KIRMIZI" for x in tehlikeli),
        "amanita_n": len(amanita), "amanita_torba_gordu": oran(amanita, lambda x: x["torba"] == "var"),
        "dusuk_n": len(dusuk),
        "dusuk_gri_once": oran(dusuk, lambda x: x["once"] == "GRI"), "dusuk_gri_sonra": oran(dusuk, lambda x: x["sonra"] == "GRI"),
        "dusuk_gemma_kirmizi": oran(dusuk, lambda x: x["kirmiziya_cek"]),
        "negatif_n": len(negatif),
        "negatif_red_once": oran(negatif, lambda x: x["once"] == "MANTAR_DEGIL"),
        "negatif_red_sonra": oran(negatif, lambda x: x["sonra"] == "MANTAR_DEGIL"),
    }
    RES.mkdir(exist_ok=True)
    (RES / "gemma_degerlendirme.json").write_text(json.dumps({"ozet": m, "fotograflar": sonuc}, ensure_ascii=False, indent=1), encoding="utf-8")
    rapor(m, sonuc)
    print(json.dumps(m, ensure_ascii=False, indent=1))


def yuzde(v):
    return "—" if v is None else f"{v:.0%}"


def rapor(m, sonuc):
    kurtarilan = [x for x in sonuc if x["risk"] in TEHLIKELI and x["once"] != "KIRMIZI" and x["sonra"] == "KIRMIZI"]
    gereksiz = [x for x in sonuc if x["risk"] == "dusuk" and x["kirmiziya_cek"]]
    L = ["# Gemma 4'ün katkısı", "",
         f"Modelin eğitimde hiç görmediği **{m['foto_sayisi']} test fotoğrafı**, iki yoldan geçirildi: (A) yalnızca görüntü modeli + "
         "güvenlik kuralları, (B) A + Gemma 4 görsel özellik analizi. Gemma kuralı riski yalnızca yükseltebilir. "
         f"Her fotoğraf tek açıdan çekilmiştir (uygulamada üç açı önerilir). Gemma hatası: {m['gemma_hata']}.", "",
         "| Metrik | Yalnızca model | Model + Gemma 4 |", "|---|---:|---:|",
         f"| Zehirli/ölümcül tür → **KIRMIZI** (n={m['tehlikeli_n']}) | {yuzde(m['tehlikeli_kirmizi_once'])} | **{yuzde(m['tehlikeli_kirmizi_sonra'])}** |",
         f"| Zehirli/ölümcül tür → 'düşük riskli aday' (**tehlikeli karışıklık**) | {yuzde(m['tehlikeli_gri_once'])} | **{yuzde(m['tehlikeli_gri_sonra'])}** |",
         f"| Düşük riskli tür → GRİ (gereksiz alarm olmaması, n={m['dusuk_n']}) | {yuzde(m['dusuk_gri_once'])} | {yuzde(m['dusuk_gri_sonra'])} |",
         f"| Mantar olmayan fotoğraf reddedildi (n={m['negatif_n']}) | {yuzde(m['negatif_red_once'])} | {yuzde(m['negatif_red_sonra'])} |",
         "", f"- Gemma'nın KIRMIZI'ya çektiği zehirli tür fotoğrafı: **{m['tehlikeli_kurtarilan']}**",
         f"- Amanita (köygöçüren, panter, sinek mantarı) fotoğraflarında Gemma'nın sap tabanında torba görme oranı: **{yuzde(m['amanita_torba_gordu'])}** (n={m['amanita_n']})",
         f"- Düşük riskli türlerde Gemma'nın riski KIRMIZI'ya çektiği oran (bedel): **{yuzde(m['dusuk_gemma_kirmizi'])}**", ""]
    if kurtarilan:
        L += ["## Gemma'nın yakaladığı örnekler", "", "| Fotoğraf | Gerçek tür | Model ne dedi | Önce | Sonra |", "|---|---|---|---|---|"]
        L += [f"| [{x['photo_id']}](https://www.inaturalist.org/observations/{x['observation_id']}) | *{x['sinif']}* | *{x['model_ilk']}* | {x['once']} | {x['sonra']} |" for x in kurtarilan[:12]]
    if gereksiz:
        L += ["", "## Gereksiz alarm örnekleri (düşük riskli tür, Gemma KIRMIZI)", "", "| Fotoğraf | Gerçek tür | Gemma torba |", "|---|---|---|"]
        L += [f"| [{x['photo_id']}](https://www.inaturalist.org/observations/{x['observation_id']}) | *{x['sinif']}* | {x['torba']} |" for x in gereksiz[:12]]
    L += ["", "Asimetrik maliyet: zehirliyi kaçırmak ölümcül olabilir; düşük riskli bir mantarda gereksiz alarm en fazla boş sepettir.", ""]
    (RES / "gemma_degerlendirme.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
