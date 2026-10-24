// MycoGuard karar katmanı — src/decide.py ile birebir aynı kural (tests/test_parity.py doğrular).
// Tarayıcıda window.MycoDecide, Node'da require("./decide.js") olarak kullanılır.
(function (root) {
  const DANGER_RISKS_DEFAULT = ["olumcul", "yuksek"];

  // case: { mantar_olma_olasiligi, simule_top5: [{latin_name, p}] }
  // info: { latin_name: {risk, ...} }, T: eşikler (demo_cases.json "esikler")
  function decide(c, info, T) {
    if (c.mantar_olma_olasiligi < T.mantar_degil_esigi) return { level: "MANTAR_DEGIL", danger: [] };
    const top5 = c.simule_top5;
    const risky = T.tehlikeli_risk_seviyeleri || DANGER_RISKS_DEFAULT;
    const danger = top5.filter(x => x.p >= T.tehlikeli_aday_min_olasilik && risky.includes(info[x.latin_name].risk));
    if (danger.length) return { level: "KIRMIZI", danger };
    const top1 = top5[0];
    if (top1.p < T.belirsizlik_esigi) return { level: "SARI", reason: "belirsiz", danger: [] };
    if (info[top1.latin_name].risk === "orta") return { level: "SARI", reason: "sartli", danger: [] };
    return { level: "GRI", danger: [] };
  }

  // Gemma 4 görsel bulguları riski yalnızca YÜKSELTİR, asla düşürmez.
  // g: /api/analiz yanıtı { ozellikler, kirmiziya_cek, uyarilar }
  const RANK = { GRI: 0, SARI: 1, KIRMIZI: 2 };
  function escalate(d, g) {
    if (!g || !g.ozellikler) return d;
    const oz = g.ozellikler;
    if (d.level === "MANTAR_DEGIL")
      return oz.mantar_mi ? { ...d, level: g.kirmiziya_cek ? "KIRMIZI" : "SARI", reason: "gemma_mantar", escalated: true } : d;
    if (g.kirmiziya_cek && RANK[d.level] < RANK.KIRMIZI) return { ...d, level: "KIRMIZI", reason: "gemma_ozellik", escalated: true };
    if (oz.foto_kalitesi === "kotu" && d.level === "GRI") return { ...d, level: "SARI", reason: "gemma_kalite", escalated: true };
    return d;
  }

  const api = { decide, escalate };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.MycoDecide = api;
})(typeof window !== "undefined" ? window : globalThis);
