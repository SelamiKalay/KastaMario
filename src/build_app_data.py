"""data/ klasöründeki CSV ve JSON'u app/data.js'e gömer.

Böylece app/index.html internetsiz ve sunucusuz (çift tıklayarak) açılır.
Veriyi değiştirdikten sonra çalıştırın:

    python src/build_app_data.py
"""
import json
from pathlib import Path

from decide import DATA, ROOT, load

cfg, info = load()
out = ROOT / "app" / "data.js"
out.write_text(
    "// OTOMATİK ÜRETİLDİ: python src/build_app_data.py — elle düzenlemeyin.\n"
    f"window.MYCO_CASES = {json.dumps(cfg, ensure_ascii=False, indent=1)};\n"
    f"window.MYCO_SPECIES = {json.dumps(list(info.values()), ensure_ascii=False, indent=1)};\n",
    encoding="utf-8",
)
print(f"{out.relative_to(ROOT)} yazıldı ({len(info)} tür, {len(cfg['senaryolar'])} senaryo)")
