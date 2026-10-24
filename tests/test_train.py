"""Eğitim veri hattının hafif testleri (yalnızca CPU, küçük rastgele veri; model eğitilmez)."""
import json

import numpy as np
import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("torchvision")
from PIL import Image  # noqa: E402

import train  # noqa: E402


def test_kare_256_kisa_kenar_ve_orta_kirpma(tmp_path):
    # 400x300: sol yarı kırmızı, sağ yarı mavi; ortadan kırpılınca iki renk de görünmeli
    im = np.zeros((300, 400, 3), np.uint8)
    im[:, :200, 0], im[:, 200:, 2] = 255, 255
    Image.fromarray(im).save(tmp_path / "a.jpg", quality=95)
    out = train.kare_256(tmp_path / "a.jpg")
    assert out.shape == (256, 256, 3) and out.dtype == np.uint8
    assert out[128, 10, 0] > 200 and out[128, 245, 2] > 200


def test_onbellek_yeniden_kullanir(tmp_path, monkeypatch):
    for i in range(3):
        Image.fromarray(np.full((50, 80, 3), i * 60, np.uint8)).save(tmp_path / f"{i}.jpg")
    monkeypatch.setattr(train, "IMG", tmp_path)
    rows = [{"photo_id": str(i)} for i in range(3)]
    X = train.onbellek(rows, dizin=tmp_path / "c")
    assert X.shape == (3, 256, 256, 3) and json.loads((tmp_path / "c" / "fotolar_256.json").read_text()) == ["0", "1", "2"]
    monkeypatch.setattr(train, "kare_256", lambda p: (_ for _ in ()).throw(AssertionError("önbellek kullanılmadı")))
    assert np.array_equal(train.onbellek(rows, dizin=tmp_path / "c"), X)


def test_artir_boyut_aralik_ve_cesitlilik():
    g = torch.Generator().manual_seed(0)
    x = torch.rand(8, 3, 256, 256, generator=g)
    a, b = train.artir(x, gen=g), train.artir(x, gen=g)
    assert a.shape == (8, 3, 224, 224) and a.min() >= 0 and a.max() <= 1
    assert not torch.allclose(a, b), "her çağrıda farklı rastgele artırma"


def test_test_goruntu_tum_kareyi_224e_olcekler():
    x = torch.zeros(2, 3, 256, 256)
    x[..., :, :128] = 1
    y = train.test_goruntu(x)
    assert y.shape == (2, 3, 224, 224)
    assert y[0, 0, 100, 5] > 0.99 and y[0, 0, 100, 218] < 0.01, "kırpmadan tüm kare kullanılmalı"


def test_gpuveri_toplulari_ve_normalize():
    X = np.random.default_rng(0).integers(0, 255, (10, 256, 256, 3), dtype=np.uint8)
    egit = train.GPUVeri(X, list(range(10)), "cpu", 4, egitim=True)
    test = train.GPUVeri(X, list(range(10)), "cpu", 4, egitim=False)
    assert len(egit) == 2 and len(test) == 3, "eğitimde eksik son toplu atılır, testte tümü kullanılır"
    xb, yb = next(iter(test))
    assert xb.shape == (4, 3, 224, 224) and yb.tolist() == [0, 1, 2, 3]
    assert -3 < xb.mean().item() < 3, "ImageNet normalizasyonu uygulanmış olmalı"
    assert sorted(t for _, y in test for t in y.tolist()) == list(range(10))
