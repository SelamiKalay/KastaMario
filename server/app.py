"""MycoGuard sunucusu: app/ klasörünü sunar ve Gemma 4 uç noktalarını sağlar (bağımlılıksız).

    python server/app.py            # http://localhost:8000

Uç noktalar:
    GET  /api/durum    -> Gemma hazır mı?
    POST /api/analiz   {image: base64, adaylar: [ad], seviye}  -> görsel özellikler + risk yükseltme
    POST /api/sohbet   {mesajlar: [...], baglam: {...}}         -> bilgi tabanına dayalı yanıt
"""
import json
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import gemma  # noqa: E402
from decide import load  # noqa: E402

_, INFO = load()
MAX_BODY = 12 * 1024 * 1024


class Handler(SimpleHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/durum":
            return self._json(200, gemma.durum())
        return super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            return self._json(413, {"hata": "istek çok büyük"})
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/api/analiz":
                oz = gemma.gorsel_ozellikler(body["image"])
                return self._json(200, {"ozellikler": oz, **gemma.risk_yukseltme(oz, INFO, body.get("adaylar", []))})
            if self.path == "/api/sohbet":
                return self._json(200, gemma.sohbet(INFO, body["mesajlar"], body.get("baglam", {})))
            return self._json(404, {"hata": "bulunamadı"})
        except (KeyError, ValueError) as e:
            return self._json(400, {"hata": f"geçersiz istek: {e}"})
        except OSError as e:
            return self._json(503, {"hata": f"Gemma'ya ulaşılamadı ({gemma.OLLAMA}): {e}"})

    def log_message(self, fmt, *args):
        if self.path.startswith("/api/"):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))
    srv = ThreadingHTTPServer(("0.0.0.0", port), partial(Handler, directory=str(ROOT / "app")))
    print(f"MycoGuard: http://localhost:{port}  |  Gemma: {gemma.MODEL} @ {gemma.OLLAMA} -> {gemma.durum()}", flush=True)
    srv.serve_forever()
