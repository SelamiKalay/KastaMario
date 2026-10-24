"""Uygulama dosyalarının telefonda/tarayıcıda yüklenebilirliğini koruyan testler (ikisi de gerçek hatalardan çıktı)."""
import re

from decide import ROOT

APP = ROOT / "app"
HTML = (APP / "index.html").read_text(encoding="utf-8")


def test_onnx_wasm_yolu_tam_adres():
    # ORT .mjs dosyasını import() ile yükler; "vendor/ort/" gibi göreli ad modül adı sanılıp reddediliyordu
    # ("Failed to resolve module specifier") ve görüntü modeli hiç yüklenmiyordu.
    js = (APP / "model.js").read_text(encoding="utf-8")
    assert 'wasmPaths = new URL("vendor/ort/", location.href).href' in js
    assert not re.search(r'wasmPaths\s*=\s*"vendor/', js)


def test_yerel_dosyalar_surum_etiketli_ve_var():
    # Sürümsüz adresler telefonda eski önbellek kopyasına takılıyordu (python src/build_app_data.py ekler).
    refs = re.findall(r'(?:src|href)="((?:config|data|decide|model)\.js|vendor/ort/ort\.wasm\.min\.js|fonts/fonts\.css)([^"]*)"', HTML)
    assert len(refs) == 6
    for yol, sorgu in refs:
        assert re.fullmatch(r"\?v=[0-9a-f]{8}", sorgu), yol
        assert (APP / yol).exists(), yol


def test_html_deki_yerel_gorseller_mevcut():
    for yol in re.findall(r'(?:src|href)="((?:img/|icon|favicon|apple-touch)[^"?]+)"', HTML):
        assert (APP / yol).exists(), yol
