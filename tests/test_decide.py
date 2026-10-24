import pytest

from decide import decide, load

CFG, INFO = load()
T = CFG["esikler"]


def case(top, mantar=0.95):
    return {"mantar_olma_olasiligi": mantar, "simule_top5": [{"latin_name": n, "p": p} for n, p in top]}


@pytest.mark.parametrize("c", CFG["senaryolar"], ids=lambda c: c["id"])
def test_demo_senaryolari(c):
    assert decide(c, INFO, T) == c["beklenen_seviye"]


def test_en_kotu_aday_kurali_birinci_tahmini_ezer():
    # Birinci aday %90 düşük riskli, ama %5'lik ölümcül aday varsa yine KIRMIZI.
    c = case([("Agaricus campestris", 0.90), ("Amanita phalloides", 0.05), ("Boletus edulis", 0.05)])
    assert decide(c, INFO, T) == "KIRMIZI"


def test_tehlikeli_aday_esigin_altindaysa_kirmizi_degil():
    c = case([("Pleurotus ostreatus", 0.96), ("Omphalotus olearius", 0.04)])
    assert decide(c, INFO, T) == "GRI"


@pytest.mark.parametrize("p,beklenen", [(0.5999, "SARI"), (0.60, "GRI")])
def test_belirsizlik_esigi_siniri(p, beklenen):
    c = case([("Boletus edulis", p), ("Cantharellus cibarius", 1 - p)])
    assert decide(c, INFO, T) == beklenen


@pytest.mark.parametrize("m,beklenen", [(0.4999, "MANTAR_DEGIL"), (0.50, "GRI")])
def test_mantar_degil_esigi_siniri(m, beklenen):
    assert decide(case([("Boletus edulis", 0.9)], mantar=m), INFO, T) == beklenen


def test_mantar_degilse_tehlikeli_aday_olsa_bile_reddeder():
    assert decide(case([("Amanita phalloides", 0.9)], mantar=0.1), INFO, T) == "MANTAR_DEGIL"


def test_sartli_tur_yuksek_guvende_bile_sari():
    assert decide(case([("Morchella esculenta", 0.97), ("Boletus edulis", 0.03)]), INFO, T) == "SARI"


@pytest.mark.parametrize("ad", [s for s, r in INFO.items() if r["risk"] in ("olumcul", "yuksek")])
def test_her_tehlikeli_tur_birinci_adaysa_kirmizi(ad):
    assert decide(case([(ad, 0.7), ("Boletus edulis", 0.3)]), INFO, T) == "KIRMIZI"


def test_hicbir_cikti_guvenli_demez():
    seviyeler = {decide(c, INFO, T) for c in CFG["senaryolar"]}
    assert seviyeler <= {"KIRMIZI", "SARI", "GRI", "MANTAR_DEGIL"}
