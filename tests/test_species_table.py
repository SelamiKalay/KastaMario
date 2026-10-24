import csv
import re

import pytest

from decide import DATA, load

CFG, INFO = load()
ROWS = list(INFO.values())
KOLONLAR = ["id", "latin_name", "turkce_ad", "yerel_ad", "risk", "zehir_notu", "belirtiler", "belirti_baslangici",
            "belirti_saat_min", "belirti_saat_max", "ilk_yardim_notu", "habitat", "substrat", "kastamonu_notu",
            "sapka_cm", "sap_cm", "yetisme_sureci", "mevsim", "aylar", "toplama_notu", "ikiz_turler",
            "ayirt_edici_ipucu", "dogrulama_durumu", "kaynak"]


def test_kolonlar_ve_satir_sayisi():
    with open(DATA / "species_info.csv", encoding="utf-8") as f:
        r = csv.reader(f)
        assert next(r) == KOLONLAR
        satirlar = list(r)
    assert all(len(s) == len(KOLONLAR) for s in satirlar)
    assert len(satirlar) == len(INFO), "latin_name tekrar ediyor"


def test_idler_benzersiz():
    assert len({r["id"] for r in ROWS}) == len(ROWS)


@pytest.mark.parametrize("r", ROWS, ids=lambda r: r["id"])
def test_satir_gecerli(r):
    assert r["risk"] in {"olumcul", "yuksek", "orta", "dusuk"}
    assert re.fullmatch(r"[A-Z][a-z]+ [a-z]+", r["latin_name"])
    aylar = [int(a) for a in r["aylar"].split(";")]
    assert aylar and all(1 <= a <= 12 for a in aylar) and len(set(aylar)) == len(aylar)
    for k in ("turkce_ad", "zehir_notu", "belirtiler", "habitat", "ayirt_edici_ipucu", "kastamonu_notu",
              "yetisme_sureci", "toplama_notu", "ilk_yardim_notu"):
        assert r[k].strip(), f"{k} boş"
    assert re.match(r"^\d+-\d+", r["sapka_cm"]) and re.match(r"^\d+-\d+", r["sap_cm"])
    assert r["ikiz_turler"] and r["latin_name"] not in r["ikiz_turler"].split(";")


@pytest.mark.parametrize("r", [r for r in ROWS if r["risk"] != "dusuk"], ids=lambda r: r["id"])
def test_riskli_turlerde_belirti_suresi_sayisal(r):
    mn, mx = float(r["belirti_saat_min"]), float(r["belirti_saat_max"])
    assert 0 < mn <= mx <= 24 * 30


@pytest.mark.parametrize("r", [r for r in ROWS if r["risk"] in ("olumcul", "yuksek")], ids=lambda r: r["id"])
def test_tehlikeli_turler_toplanmaz(r):
    assert r["toplama_notu"].startswith("Toplanmaz")


def test_amatoksinli_turler_gecikmeli():
    for ad in ("Amanita phalloides", "Amanita virosa", "Galerina marginata", "Lepiota brunneoincarnata"):
        assert float(INFO[ad]["belirti_saat_min"]) >= 6


def test_dusuk_risk_asla_guvenli_demez():
    for r in ROWS:
        metin = " ".join(r.values()).lower()
        assert not re.search(r"\b(güvenlidir|yenilebilir\.|zehirsizdir)\b", metin), r["latin_name"]


def test_her_tehlikeli_tur_bir_dusuk_riskli_turun_ikizi_ya_da_ikizi_var():
    # Uygulamanın "Bunu sakın karıştırma" kartı tehlikeli türler için en az bir eşleşme bulabilmeli.
    for r in ROWS:
        if r["risk"] in ("olumcul", "yuksek"):
            ikizi = any(t in INFO for t in r["ikiz_turler"].split(";"))
            ikiz_olarak_gecer = any(r["latin_name"] in o["ikiz_turler"].split(";") for o in ROWS)
            assert ikizi or ikiz_olarak_gecer, r["latin_name"]


def test_senaryolardaki_turler_tabloda():
    for c in CFG["senaryolar"]:
        for x in c["simule_top5"]:
            assert x["latin_name"] in INFO
        assert abs(sum(x["p"] for x in c["simule_top5"]) - 1) < 0.02
