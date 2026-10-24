"""Gemma 4 katmanının güvenlik kuralları (Ollama gerekmez; model yanıtları taklit edilir)."""
import json
import shutil
import subprocess
import sys

import pytest

from decide import ROOT, load

sys.path.insert(0, str(ROOT / "server"))
import gemma  # noqa: E402

CFG, INFO = load()
NODE = shutil.which("node")


def oz(**k):
    base = {"mantar_mi": True, "alt_yuz": "lamel", "lamel_rengi": "kahverengi", "sapta_halka": "yok",
            "sap_tabaninda_torba": "yok", "yetistigi_yer": "toprak", "kumeler_halinde": "hayir",
            "foto_kalitesi": "iyi", "eksik_acilar": [], "aciklama": ""}
    return {**base, **k}


def test_torba_gorulurse_kirmiziya_ceker():
    r = gemma.risk_yukseltme(oz(sap_tabaninda_torba="var"), INFO, ["Agaricus campestris"])
    assert r["kirmiziya_cek"] and "torba" in r["uyarilar"][0]


def test_beyaz_lamel_ve_halka_kirmiziya_ceker():
    assert gemma.risk_yukseltme(oz(lamel_rengi="beyaz", sapta_halka="var"), INFO, [])["kirmiziya_cek"]


def test_masum_ozellikler_risk_yukseltmez():
    r = gemma.risk_yukseltme(oz(), INFO, ["Agaricus campestris"])
    assert not r["kirmiziya_cek"]


def test_sap_tabani_gorunmuyorsa_yeni_foto_ister():
    r = gemma.risk_yukseltme(oz(sap_tabaninda_torba="gorunmuyor"), INFO, [])
    assert any("sap tabanını" in u for u in r["uyarilar"])


def test_petek_sapka_kesit_uyarisi():
    assert any("boyuna kes" in u for u in gemma.risk_yukseltme(oz(alt_yuz="petek"), INFO, [])["uyarilar"])


def test_sohbet_yasak_ifadeleri_suzer(monkeypatch):
    monkeypatch.setattr(gemma, "_post", lambda *a, **k: {"message": {"content": "Bu mantar yenilebilir, gönül rahatlığıyla yiyebilirsin."}})
    c = gemma.sohbet(INFO, [{"role": "user", "content": "sarıkız yenir mi"}], {})["cevap"]
    assert "yenilebilir" not in c.split("⚠️")[0] and "yiyebilirsin" not in c
    assert "uzman onayı" in c


def test_sohbet_bilgi_tabanini_ve_kurallari_gonderir(monkeypatch):
    giden = {}

    def sahte(path, body, **k):
        giden.update(body)
        return {"message": {"content": "Hemen 112 / 114'ü arayın."}}
    monkeypatch.setattr(gemma, "_post", sahte)
    r = gemma.sohbet(INFO, [{"role": "user", "content": "Köygöçüren yedim galiba"}], {"seviye": "KIRMIZI", "adaylar": []})
    sistem = giden["messages"][0]["content"]
    assert "Amanita phalloides" in r["kaynak_turler"]
    assert "BİLGİ TABANI" in sistem and "yenilebilir" in sistem and "Amatoksin" in sistem
    assert "KIRMIZI" in sistem


def test_gorsel_ozellik_istegi_semali_ve_deterministik(monkeypatch):
    giden = {}

    def sahte(path, body, **k):
        giden.update(body)
        return {"message": {"content": json.dumps(oz(sap_tabaninda_torba="var"))}}
    monkeypatch.setattr(gemma, "_post", sahte)
    out = gemma.gorsel_ozellikler("QUJD")
    assert out["sap_tabaninda_torba"] == "var"
    assert giden["format"] == gemma.OZELLIK_SEMASI and giden["options"]["temperature"] == 0
    assert giden["messages"][0]["images"] == ["QUJD"]


def test_ollama_yoksa_durum_hazir_degil(monkeypatch):
    monkeypatch.setattr(gemma, "OLLAMA", "http://127.0.0.1:9")
    assert gemma.durum() == {"ollama": False, "model": gemma.MODEL, "hazir": False}


@pytest.mark.skipif(not NODE, reason="node kurulu değil")
def test_js_escalate_riski_asla_dusurmez():
    seviyeler = ["GRI", "SARI", "KIRMIZI", "MANTAR_DEGIL"]
    bulgular = [None, {"ozellikler": oz(), "kirmiziya_cek": False}, {"ozellikler": oz(), "kirmiziya_cek": True},
                {"ozellikler": oz(foto_kalitesi="kotu"), "kirmiziya_cek": False},
                {"ozellikler": oz(mantar_mi=False), "kirmiziya_cek": False}]
    js = ("const {escalate}=require(process.argv[1]);const L=JSON.parse(process.argv[2]),G=JSON.parse(process.argv[3]);"
          "console.log(JSON.stringify(L.map(l=>G.map(g=>escalate({level:l,danger:[]},g).level))))")
    out = json.loads(subprocess.run([NODE, "-e", js, str(ROOT / "app" / "decide.js"), json.dumps(seviyeler), json.dumps(bulgular)],
                                    capture_output=True, text=True, check=True).stdout)
    rank = {"MANTAR_DEGIL": -1, "GRI": 0, "SARI": 1, "KIRMIZI": 2}
    for l, satir in zip(seviyeler, out):
        for yeni in satir:
            assert rank[yeni] >= rank[l], (l, yeni)
    assert out[0][2] == "KIRMIZI" and out[0][3] == "SARI" and out[2] == ["KIRMIZI"] * 5
