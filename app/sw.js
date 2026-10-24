// Çevrimdışı çalışma: önce ağ, ağ yoksa önbellek (güncel veri her zaman öncelikli).
const CACHE = "kastamario-v1";
const FILES = ["./", "index.html", "config.js", "data.js", "decide.js", "model.js", "manifest.webmanifest", "favicon.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "img/kastamario-96.png", "img/mybear-128.png", "img/anatomi.jpg", "fonts/fonts.css", "fonts/IBMPlexSans-latin-1.woff2", "fonts/IBMPlexSans-latin-ext-0.woff2", "fonts/Newsreader-latin-3.woff2", "fonts/Newsreader-latin-5.woff2", "fonts/Newsreader-latin-ext-2.woff2", "fonts/Newsreader-latin-ext-4.woff2",
  "vendor/ort/ort.wasm.min.js", "vendor/ort/ort-wasm-simd-threaded.wasm", "vendor/ort/ort-wasm-simd-threaded.mjs",
  "model/labels.json", "model/mycoguard.onnx"];

self.addEventListener("install", e => e.waitUntil(
  caches.open(CACHE).then(c => Promise.allSettled(FILES.map(f => c.add(f)))).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || new URL(e.request.url).pathname.includes("/api/")) return;
  e.respondWith(fetch(e.request).then(r => {
    const copy = r.clone();
    caches.open(CACHE).then(c => c.put(e.request, copy));
    return r;
  }).catch(() => caches.match(e.request)));
});
