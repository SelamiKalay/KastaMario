"""app/decide.js ile src/decide.py aynı kararı veriyor mu? (2000 rastgele vaka + demo senaryoları)"""
import json
import random
import shutil
import subprocess

import pytest

from decide import ROOT, decide, load

CFG, INFO = load()
T = CFG["esikler"]
NODE = shutil.which("node")


def rastgele_vakalar(n=2000, seed=7):
    rng = random.Random(seed)
    adlar = list(INFO)
    out = []
    for _ in range(n):
        sec = rng.sample(adlar, 5)
        w = [rng.random() ** rng.choice([1, 3, 6]) for _ in sec]
        s = sum(w)
        top = sorted(({"latin_name": a, "p": round(x / s, 4)} for a, x in zip(sec, w)), key=lambda x: -x["p"])
        out.append({"mantar_olma_olasiligi": round(rng.random(), 3), "simule_top5": top})
    return out + CFG["senaryolar"]


@pytest.mark.skipif(not NODE, reason="node kurulu değil")
def test_python_ve_js_ayni_karari_verir(tmp_path):
    vakalar = rastgele_vakalar()
    (tmp_path / "in.json").write_text(json.dumps({"cases": vakalar, "info": INFO, "T": T}), encoding="utf-8")
    js = ("const {decide}=require(process.argv[1]);const d=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));"
          "console.log(JSON.stringify(d.cases.map(c=>decide(c,d.info,d.T).level)))")
    out = subprocess.run([NODE, "-e", js, str(ROOT / "app" / "decide.js"), str(tmp_path / "in.json")],
                         capture_output=True, text=True, check=True).stdout
    js_sonuc = json.loads(out)
    py_sonuc = [decide(c, INFO, T) for c in vakalar]
    farkli = [(i, p, j) for i, (p, j) in enumerate(zip(py_sonuc, js_sonuc)) if p != j]
    assert not farkli, farkli[:5]
    assert len(set(py_sonuc)) == 4, "rastgele vakalar dört seviyeyi de kapsamalı"


@pytest.mark.skipif(not NODE, reason="node kurulu değil")
def test_escalate_python_ve_js_ayni():
    from decide import escalate
    oz = lambda **k: {"mantar_mi": True, "foto_kalitesi": "iyi", **k}  # noqa: E731
    bulgular = [None, {}, {"ozellikler": oz(), "kirmiziya_cek": False}, {"ozellikler": oz(), "kirmiziya_cek": True},
                {"ozellikler": oz(foto_kalitesi="kotu"), "kirmiziya_cek": False},
                {"ozellikler": oz(mantar_mi=False), "kirmiziya_cek": True}, {"ozellikler": oz(mantar_mi=True), "kirmiziya_cek": True}]
    seviyeler = ["GRI", "SARI", "KIRMIZI", "MANTAR_DEGIL"]
    js = ("const {escalate}=require(process.argv[1]);const L=JSON.parse(process.argv[2]),G=JSON.parse(process.argv[3]);"
          "console.log(JSON.stringify(L.map(l=>G.map(g=>escalate({level:l,danger:[]},g).level))))")
    out = json.loads(subprocess.run([NODE, "-e", js, str(ROOT / "app" / "decide.js"), json.dumps(seviyeler), json.dumps(bulgular)],
                                    capture_output=True, text=True, check=True).stdout)
    assert out == [[escalate(l, g) for g in bulgular] for l in seviyeler]
