"""KastaMario sunucusu: app/ klasörünü sunar ve Gemma 4 uç noktalarını sağlar (bağımlılıksız).

    GEMINI_API_KEY=... python server/app.py          # http://localhost:8000

Uç noktalar (mobil uygulama için CORS açık):
    GET  /api/durum    -> asistan hazır mı?
    POST /api/analiz   {images: [base64, ...] (1-3 açı)}      -> görsel özellikler + risk yükseltme
    POST /api/sohbet   {mesajlar: [...], baglam: {...}}       -> bilgi tabanına dayalı yanıt
    POST /api/sohbet-akis  (aynı gövde)                       -> yanıt parça parça (NDJSON: {"t": ...} ... {"son": true})
"""
import json
import os
import sys
import time
from collections import defaultdict, deque
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "server")]


def env_yukle(path):
    """KEY=deger satırlarını ortam değişkenlerine yükler (zaten tanımlı olanları ezmez). .env git'e girmez."""
    if not path.exists():
        return
    for satir in path.read_text(encoding="utf-8-sig").splitlines():
        k, sep, v = satir.strip().partition("=")
        if sep and k and not k.startswith("#"):
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


env_yukle(ROOT / ".env")
import gemma  # noqa: E402
from decide import load  # noqa: E402

_, INFO = load()
MAX_BODY = 8 * 1024 * 1024
LIMIT, PENCERE = int(os.environ.get("MYCOGUARD_RATE", 30)), 600   # IP başına 10 dakikada en fazla istek
CORS = os.environ.get("MYCOGUARD_CORS", "*")
_istekler = defaultdict(deque)


def sinir_asildi(ip, simdi=None):
    simdi = simdi or time.time()
    q = _istekler[ip]
    while q and q[0] < simdi - PENCERE:
        q.popleft()
    if len(q) >= LIMIT:
        return True
    q.append(simdi)
    return False


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.startswith("/api/"):
            self.send_header("Access-Control-Allow-Origin", CORS)
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _akis(self, olaylar):
        """Her satırı bir JSON olay olan akış (NDJSON). İlk parça gelmeden hata olursa normal 503 döner."""
        olaylar = iter(olaylar)
        ilk = next(olaylar)   # API hatası burada yakalanır (do_POST'taki except)
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        try:
            for olay in [ilk] if ilk else []:
                self.wfile.write((json.dumps(olay, ensure_ascii=False) + "\n").encode())
            for olay in olaylar:
                self.wfile.write((json.dumps(olay, ensure_ascii=False) + "\n").encode())
                self.wfile.flush()
        except gemma.LLMHatasi as e:
            self.log_error("LLM akış: %s", e)
            self.wfile.write((json.dumps({"hata": "Yanıt yarıda kesildi; lütfen tekrar deneyin."}, ensure_ascii=False) + "\n").encode())
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass   # kullanıcı paneli kapattı

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/durum":
            return self._json(200, gemma.durum())
        return super().do_GET()

    def do_POST(self):
        ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
        if sinir_asildi(ip):
            return self._json(429, {"hata": "Çok fazla istek; lütfen birkaç dakika sonra tekrar deneyin."})
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            return self._json(413, {"hata": "İstek çok büyük"})
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/api/analiz":
                images = body.get("images") or [body["image"]]
                if not isinstance(images, list) or not all(isinstance(b, str) and b for b in images):
                    raise ValueError("images bir base64 listesi olmalı")
                oz = gemma.gorsel_ozellikler(images[:3])
                return self._json(200, {"ozellikler": oz, "foto_sayisi": min(3, len(images)), **gemma.risk_yukseltme(oz)})
            if self.path == "/api/sohbet":
                return self._json(200, gemma.sohbet(INFO, body["mesajlar"], body.get("baglam", {})))
            if self.path == "/api/sohbet-akis":
                return self._akis(gemma.sohbet_akis(INFO, body["mesajlar"], body.get("baglam", {})))
            return self._json(404, {"hata": "Bulunamadı"})
        except (KeyError, ValueError, TypeError) as e:
            return self._json(400, {"hata": f"Geçersiz istek: {e}"})
        except gemma.LLMHatasi as e:
            self.log_error("LLM: %s", e)
            return self._json(503, {"hata": "Asistan şu an yanıt veremiyor; lütfen tekrar deneyin."})

    def log_message(self, fmt, *args):
        if self.path.startswith("/api/"):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))
    srv = ThreadingHTTPServer(("0.0.0.0", port), partial(Handler, directory=str(ROOT / "app")))
    print(f"KastaMario: http://localhost:{port}  |  asistan: {gemma.durum()}", flush=True)
    srv.serve_forever()
