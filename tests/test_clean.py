"""Veri temizleme fonksiyonlarının kirli örnek veriyle testleri."""
from collections import Counter, defaultdict

import numpy as np
import pytest
from PIL import Image, ImageFilter

import clean


@pytest.mark.parametrize("girdi,beklenen", [
    ("Kastamonu", "kastamonu"), ("KASTAMONU", "kastamonu"), ("Kastamonu İli", "kastamonu"),
    ("Kastamonu Province", "kastamonu"), (" kastamonu ", "kastamonu"), ("İSTANBUL", "istanbul"),
    ("Çankırı", "cankiri"), ("", ""), (None, ""), ("Province", ""),
])
def test_il_adi_normalizasyonu(girdi, beklenen):
    assert clean.tr_normalize(girdi) == beklenen


@pytest.mark.parametrize("girdi,beklenen", [
    ("Amanita muscaria", "Amanita muscaria"), ("Amanita muscaria var. formosa", "Amanita muscaria"),
    ("Morchella esculenta (L.) Pers.", "Morchella esculenta"), ("Amanita", ""), ("Amanita sect. Phalloideae", ""),
    (None, ""), ("Boletus edulis Bull.", "Boletus edulis"),
])
def test_tur_adi(girdi, beklenen):
    assert clean.tur_adi(girdi) == beklenen


@pytest.mark.parametrize("girdi,beklenen", [
    ("2021-10-03", (2021, 10)), ("2021-10-03T14:00:00Z", (2021, 10)), ("2021-7", (2021, 7)),
    ("2021-13-01", (None, None)), ("3021-01-01", (None, None)), ("dün", (None, None)), (None, (None, None)),
])
def test_tarih_ayristirma(girdi, beklenen):
    assert clean.tarih_ayristir(girdi) == beklenen


@pytest.mark.parametrize("girdi,beklenen", [
    ("41.37,33.77", (41.37, 33.77)), ("0,0", (None, None)), ("95,10", (None, None)), ("abc", (None, None)), ("", (None, None)),
])
def test_konum_ayristirma(girdi, beklenen):
    assert clean.konum_ayristir(girdi) == beklenen


def test_lisans_filtresi_buyuk_kucuk_harf_ve_bosluk():
    rows = [{"lisans": v} for v in ["CC-BY", " cc0", "all rights reserved", None, "cc-by-nc"]]
    assert [r["lisans"] for r in clean.filtre_lisans(rows)] == ["cc-by", "cc0", "cc-by-nc"]


def test_taksonomi_normalize_uyusmayani_atar():
    rows = [{"sinif": s, "gozlem_taxon_adi": t} for s, t in [
        ("Amanita muscaria", "Amanita muscaria var. flavivolvata"), ("Amanita muscaria", "Amanita pantherina"),
        ("Amanita muscaria", "Amanita"), ("mantar_degil", "Pinus nigra")]]
    out = clean.taksonomi_normalize(rows)
    assert [r["gozlem_taxon_adi"] for r in out] == ["Amanita muscaria var. flavivolvata", "Pinus nigra"]
    assert out[0]["tur"] == "Amanita muscaria"


def test_rehber_disi_siniflar_cikarilir_mantar_degil_kalir():
    rows = [{"sinif": s} for s in ["Amanita phalloides", "Clitocybe rivulosa", "mantar_degil"]]
    assert [r["sinif"] for r in clean.rehberdekiler(rows, {"Amanita phalloides"})] == ["Amanita phalloides", "mantar_degil"]


def test_taksonomi_normalize_es_anlamli_adi_kabul_eder():
    rows = [{"sinif": "Clitocybe rivulosa", "istenen_taxon_adi": "Clitocybe dealbata", "gozlem_taxon_adi": "Clitocybe dealbata"},
            {"sinif": "Clitocybe rivulosa", "istenen_taxon_adi": "Clitocybe dealbata", "gozlem_taxon_adi": "Clitocybe nebularis"}]
    assert len(clean.taksonomi_normalize(rows)) == 1


def _img(seed, size=(200, 160)):
    rng = np.random.default_rng(seed)
    return Image.fromarray(rng.integers(0, 255, (size[1], size[0], 3), dtype=np.uint8)).filter(ImageFilter.GaussianBlur(4))


def test_dhash_yeniden_boyut_ve_sikistirmaya_dayanikli(tmp_path):
    a = _img(1)
    a.resize((120, 96)).save(tmp_path / "b.jpg", quality=60)
    with Image.open(tmp_path / "b.jpg") as bb:
        d = bin(clean.dhash(a) ^ clean.dhash(bb)).count("1")
    farkli = bin(clean.dhash(a) ^ clean.dhash(_img(2))).count("1")
    assert d <= clean.NEAR_DUP_HAMMING < farkli


def test_yakin_kopyalar_sonrakini_isaretler():
    h = [clean.dhash(_img(i)) for i in range(5)]
    h.append(h[2] ^ 0b1)          # 1 bit farklı kopya
    h.append(h[0])                # birebir kopya
    assert clean.yakin_kopyalar(h) == {5, 6}


def test_goruntu_kontrol_bozuk_dosya(tmp_path):
    (tmp_path / "bozuk.jpg").write_bytes(b"jpeg degil")
    assert clean.goruntu_kontrol(tmp_path / "bozuk.jpg")[0] is False
    assert clean.goruntu_kontrol(tmp_path / "yok.jpg")[0] is False
    _img(3).save(tmp_path / "iyi.jpg")
    ok, w, h, dh = clean.goruntu_kontrol(tmp_path / "iyi.jpg")
    assert ok and (w, h) == (200, 160) and dh is not None


def _sahte_veri(n_obs=100, foto=(1, 3)):
    rng = np.random.default_rng(0)
    rows, pid = [], 0
    for s in ["A a", "B b", "C c"]:
        for o in range(n_obs):
            for _ in range(rng.integers(*foto)):
                rows.append({"sinif": s, "observation_id": f"{s}-{o}", "photo_id": pid})
                pid += 1
    return rows


def test_ayirma_gozlem_bazli_sizinti_yok_ve_oranlar():
    rows = clean.ayir(_sahte_veri())
    obs_split = defaultdict(set)
    for r in rows:
        obs_split[r["observation_id"]].add(r["split"])
    assert max(map(len, obs_split.values())) == 1
    for s in ["A a", "B b", "C c"]:
        c = Counter(next(iter(v)) for o, v in obs_split.items() if o.startswith(s))
        n = sum(c.values())
        assert abs(c["train"] / n - 0.70) < 0.03 and abs(c["test"] / n - 0.15) < 0.03
    assert [r["split"] for r in clean.ayir(_sahte_veri())] == [r["split"] for r in rows], "tohumla tekrarlanabilir olmalı"


def test_dengeleme_ust_sinir_ve_az_ornekli_sinif():
    rows = _sahte_veri() + [{"sinif": "D d", "observation_id": f"d{i}", "photo_id": 9000 + i} for i in range(5)]
    out, atilan = clean.dengele(rows, en_fazla=50, en_az=10)
    assert atilan == ["D d"]
    assert max(Counter(r["sinif"] for r in out).values()) <= 50
    secilen = {r["observation_id"] for r in out}
    assert len([r for r in rows if r["observation_id"] in secilen]) == len(out), "gözlem bütünlüğü korunmalı"
