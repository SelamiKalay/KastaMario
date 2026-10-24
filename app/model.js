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
        ort.env.wasm.wasmPaths = "vendor/ort/";
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

  // Görüntüyü kısa kenarı input_size olacak şekilde ölçekleyip ortadan kırpar, normalize eder (NCHW).
  function toTensor(img) {
    const S = meta.input_size, cv = document.createElement("canvas");
    cv.width = cv.height = S;
    const ctx = cv.getContext("2d");
    const k = S / Math.min(img.width, img.height);
    const w = img.width * k, h = img.height * k;
    ctx.drawImage(img, (S - w) / 2, (S - h) / 2, w, h);
    const px = ctx.getImageData(0, 0, S, S).data, n = S * S, out = new Float32Array(3 * n);
    for (let i = 0; i < n; i++)
      for (let c = 0; c < 3; c++) out[c * n + i] = (px[i * 4 + c] / 255 - meta.mean[c]) / meta.std[c];
    return new ort.Tensor("float32", out, [1, 3, S, S]);
  }

  async function classify(img) {
    if (!(await load())) throw new Error("model-yok");
    const res = await session.run({ [session.inputNames[0]]: toTensor(img) });
    const logits = Array.from(res[session.outputNames[0]].data).map(v => v / (meta.temperature || 1));
    const mx = Math.max(...logits), ex = logits.map(v => Math.exp(v - mx)), sum = ex.reduce((a, b) => a + b, 0);
    const probs = ex.map(v => v / sum);
    const neg = meta.classes.indexOf("mantar_degil");
    const pNot = neg >= 0 ? probs[neg] : 0;
    // Tür olasılıkları "mantar olduğu varsayımıyla" yeniden ölçeklenir (demo senaryolarındaki anlamla aynı).
    const species = meta.classes.map((c, i) => ({ latin_name: c, p: probs[i] / Math.max(1e-9, 1 - pNot) }))
      .filter((_, i) => i !== neg).sort((a, b) => b.p - a.p);
    return { mantar_olma_olasiligi: 1 - pNot, simule_top5: species.slice(0, 5) };
  }

  return { load, classify, info: () => meta };
})();
