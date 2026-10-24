// Fotoğraf -> model çıktısı. Model: app/model/mycoguard.onnx + labels.json (ml/train.py üretir).
// Çıktı biçimi demo senaryolarıyla aynıdır: { mantar_olma_olasiligi, simule_top5 }.
window.MycoModel = (function () {
  let session = null, meta = null, loading = null;

  async function load() {
    if (session) return true;
    if (!loading) loading = (async () => {
      try {
        const r = await fetch("model/labels.json", { cache: "no-cache" });
        if (!r.ok) return false;
        meta = await r.json();
        // Tam adres gerekir: ORT .mjs dosyasını import() ile yükler ve "vendor/ort/..." gibi göreli adları modül adı sanıp reddeder.
        ort.env.wasm.wasmPaths = new URL("vendor/ort/", location.href).href;
        ort.env.wasm.numThreads = 1;
        session = await ort.InferenceSession.create("model/mycoguard.onnx", { executionProviders: ["wasm"] });
        return true;
      } catch (e) {
        console.warn("Model yüklenemedi:", e);
        loading = null;
        return false;
      }
    })();
    return loading;
  }

  // Bir görüntüden 224x224 NCHW tensör üretir. bakis:
  //   "orta"  kısa kenar -> 224, ortadan kare kırpma (eğitimdeki değerlendirmeyle aynı)
  //   "tam"   görüntünün tamamı, kenarları gri dolgulu kare (mantar ortada değilse ya da geniş açılı fotoğrafta)
  //   "ayna"  orta kare, yatay aynalanmış
  function toTensor(img, bakis = "orta") {
    const S = meta.input_size, cv = document.createElement("canvas");
    cv.width = cv.height = S;
    const ctx = cv.getContext("2d");
    const k = (bakis === "tam" ? Math.max : Math.min)(S / img.width, S / img.height);
    const w = img.width * k, h = img.height * k;
    if (bakis === "tam") { ctx.fillStyle = "rgb(124,116,104)"; ctx.fillRect(0, 0, S, S); }   // ImageNet ortalama rengi
    if (bakis === "ayna") { ctx.translate(S, 0); ctx.scale(-1, 1); }
    ctx.drawImage(img, (S - w) / 2, (S - h) / 2, w, h);
    const px = ctx.getImageData(0, 0, S, S).data, n = S * S, out = new Float32Array(3 * n);
    for (let i = 0; i < n; i++)
      for (let c = 0; c < 3; c++) out[c * n + i] = (px[i * 4 + c] / 255 - meta.mean[c]) / meta.std[c];
    return new ort.Tensor("float32", out, [1, 3, S, S]);
  }

  async function olasiliklar(img, bakis) {
    const res = await session.run({ [session.inputNames[0]]: toTensor(img, bakis) });
    const logits = Array.from(res[session.outputNames[0]].data).map(v => v / (meta.temperature || 1));
    const mx = Math.max(...logits), ex = logits.map(v => Math.exp(v - mx)), sum = ex.reduce((a, b) => a + b, 0);
    return ex.map(v => v / sum);
  }

  // Çoklu bakış (test zamanı artırma): üç bakışın olasılık ortalaması. İnternetten/ekrandan alınmış, mantarın
  // ortada olmadığı ya da geniş açılı fotoğraflarda tek orta kareden daha dayanıklıdır.
  const BAKISLAR = ["orta", "tam", "ayna"];
  async function classify(img) {
    if (!(await load())) throw new Error("model-yok");
    const tek = [];
    for (const b of BAKISLAR) tek.push(await olasiliklar(img, b));
    const probs = tek[0].map((_, i) => tek.reduce((s, p) => s + p[i], 0) / tek.length);
    const neg = meta.classes.indexOf("mantar_degil");
    const pNot = neg >= 0 ? probs[neg] : 0;
    // Tür olasılıkları "mantar olduğu varsayımıyla" yeniden ölçeklenir (demo senaryolarındaki anlamla aynı).
    const species = meta.classes.map((c, i) => ({ latin_name: c, p: probs[i] / Math.max(1e-9, 1 - pNot) }))
      .filter((_, i) => i !== neg).sort((a, b) => b.p - a.p);
    return { mantar_olma_olasiligi: 1 - pNot, simule_top5: species.slice(0, 5), tum: species };
  }

  // Aynı mantarın birden fazla açısı: olasılıkların ortalaması alınır.
  async function classifyMany(imgs) {
    const sonuc = [];
    for (const img of imgs) sonuc.push(await classify(img));
    if (sonuc.length === 1) return sonuc[0];
    const top = {};
    sonuc.forEach(r => r.tum.forEach(x => top[x.latin_name] = (top[x.latin_name] || 0) + x.p / sonuc.length));
    const tum = Object.entries(top).map(([latin_name, p]) => ({ latin_name, p })).sort((a, b) => b.p - a.p);
    const mantar = sonuc.reduce((s, r) => s + r.mantar_olma_olasiligi, 0) / sonuc.length;
    return { mantar_olma_olasiligi: mantar, simule_top5: tum.slice(0, 5), tum };
  }

  return { load, classify, classifyMany, info: () => meta };
})();
