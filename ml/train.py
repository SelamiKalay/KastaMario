"""3. adım — MAKİNE ÖĞRENMESİ: mantar türü sınıflandırıcı (transfer öğrenme).

Girdi : data/clean/inat_clean.csv + data/raw/images/
Çıktı : app/model/mycoguard.onnx + labels.json   (uygulamada cihazda çalışır)
        results/metrics.json, results/egitim_raporu.md, results/*.png

Model : EfficientNet-B0 (ImageNet ön eğitimli) -> 2 aşamalı ince ayar
        1) yalnızca sınıflandırıcı katman  2) tüm ağ, düşük öğrenme oranı + cosine
Kalibrasyon: sıcaklık ölçekleme (doğrulama setinde)
Güvenlik  : test setinde karar katmanıyla birlikte değerlendirme (tehlikeli tür -> KIRMIZI oranı)

    python ml/train.py                 # varsayılan ayarlar
    python ml/train.py --epochs 4      # hızlı deneme
"""
import argparse
import csv
import json
import math
import os
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import models
from torchvision.ops import roi_align

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from decide import decide, load  # noqa: E402

IMG = ROOT / "data" / "raw" / "images"
OUT_MODEL, OUT_RES = ROOT / "app" / "model", ROOT / "results"
MEAN, STD, SIZE = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225], 224
NEG = "mantar_degil"
VERSION = "1.0"
RISKLER = ["olumcul", "yuksek", "orta", "dusuk", "mantar_degil"]
KARARLAR = ["KIRMIZI", "SARI", "GRI", "MANTAR_DEGIL"]


# Windows'ta DataLoader işçileri bu makinede adım başına ~9,5 sn harcadı (GPU %5 doluluk; GPU tek başına 0,26 sn/adım).
# Bunun yerine fotoğraflar bir kez çözülüp 256x256 olarak GPU belleğine alınır, veri artırma toplu halde GPU'da yapılır.
ONBELLEK_KENAR = 256
ONBELLEK_DIR = Path(os.environ.get("MYCOGUARD_CACHE", Path.home() / "AppData" / "Local" / "mycoguard"))  # OneDrive dışında


def kare_256(path):
    """Kısa kenarı 256'ya ölçekleyip ortadan 256x256 kırpar (uygulamadaki 'kısa kenar + orta kırpma' ile aynı içerik)."""
    with Image.open(path) as im:
        im = im.convert("RGB")
        k = ONBELLEK_KENAR / min(im.size)
        im = im.resize((max(ONBELLEK_KENAR, round(im.width * k)), max(ONBELLEK_KENAR, round(im.height * k))),
                       Image.Resampling.BILINEAR)
        l, t = (im.width - ONBELLEK_KENAR) // 2, (im.height - ONBELLEK_KENAR) // 2
        return np.asarray(im.crop((l, t, l + ONBELLEK_KENAR, t + ONBELLEK_KENAR)), dtype=np.uint8)


def onbellek(rows, dizin=ONBELLEK_DIR):
    """Tüm fotoğrafları (N, 256, 256, 3) uint8 dizisine çözer; aynı fotoğraf listesi için diskteki önbelleği yeniden kullanır."""
    ids = [r["photo_id"] for r in rows]
    dizin.mkdir(parents=True, exist_ok=True)
    npy, idj = dizin / "fotolar_256.npy", dizin / "fotolar_256.json"
    if npy.exists() and idj.exists() and json.loads(idj.read_text()) == ids:
        return np.load(npy)
    t0 = time.time()
    with ThreadPoolExecutor(8) as ex:
        X = np.stack(list(ex.map(kare_256, [IMG / f"{i}.jpg" for i in ids])))
    np.save(npy, X)
    idj.write_text(json.dumps(ids))
    print(f"Önbellek: {len(ids)} fotoğraf {time.time() - t0:.0f} sn'de çözüldü ({X.nbytes / 2**30:.1f} GB, {dizin})", flush=True)
    return X


def normalize(x):
    m = torch.tensor(MEAN, device=x.device).view(1, 3, 1, 1)
    s = torch.tensor(STD, device=x.device).view(1, 3, 1, 1)
    return (x - m) / s


def artir(x, gen=None):
    """GPU'da örnek başına: rastgele boyutlu kırpma (alan %55-100, en/boy 3/4-4/3) -> 224, yatay çevirme,
    parlaklık/kontrast ±%25, doygunluk ±%20. x: (B, 3, K, K) float [0, 1] -> (B, 3, 224, 224)."""
    B, K, d = x.shape[0], x.shape[-1], x.device
    r = lambda *s: torch.rand(*s, device=d, generator=gen)  # noqa: E731
    alan = (0.55 + 0.45 * r(B)) * K * K
    oran = torch.exp(math.log(3 / 4) + (math.log(4 / 3) - math.log(3 / 4)) * r(B))
    w, h = (alan * oran).sqrt().clamp(max=K), (alan / oran).sqrt().clamp(max=K)
    x0, y0 = r(B) * (K - w), r(B) * (K - h)
    kutu = torch.stack([torch.arange(B, device=d, dtype=x.dtype), x0, y0, x0 + w, y0 + h], 1)
    out = roi_align(x, kutu, output_size=SIZE, sampling_ratio=2, aligned=True)
    out = torch.where((r(B) < 0.5)[:, None, None, None], out.flip(-1), out)
    carpan = lambda a: 1 + (r(B, 1, 1, 1) * 2 - 1) * a  # noqa: E731
    out = out * carpan(0.25)
    ort_ = out.mean((1, 2, 3), keepdim=True)
    out = (out - ort_) * carpan(0.25) + ort_
    gri = out.mean(1, keepdim=True)
    out = (out - gri) * carpan(0.20) + gri
    return out.clamp(0, 1)


def test_goruntu(x):
    """Değerlendirme: kısa kenar + orta kare (önbellekteki içerik) -> 224. Uygulamadaki ön işlemeyle aynı içerik."""
    return F.interpolate(x, size=SIZE, mode="bilinear", antialias=True, align_corners=False)


class GPUVeri:
    """Bir ayrımın (train/val/test) fotoğrafları ana bellekte (sabitlenmiş), etiketleri GPU'da; her toplu yalnızca kendi
    fotoğraflarını GPU'ya taşır. (Tüm fotoğrafları GPU'da tutmak, tüm ağ eğitilirken 8 GB'ı aşıp sistemi yavaşlattı.)"""

    def __init__(self, X, y, dev, bs, egitim):
        self.X = torch.from_numpy(np.ascontiguousarray(X))           # uint8 (N, K, K, 3), CPU
        if torch.device(dev).type == "cuda":
            self.X = self.X.pin_memory()
        self.y = torch.tensor(y, device=dev)
        self.dev, self.bs, self.egitim = dev, bs, egitim

    def __len__(self):
        n = len(self.y)
        return n // self.bs if self.egitim else math.ceil(n / self.bs)

    def __iter__(self):
        n = len(self.y)
        sira = torch.randperm(n) if self.egitim else torch.arange(n)
        for i in range(len(self)):
            idx = sira[i * self.bs:(i + 1) * self.bs]
            x = self.X[idx].to(self.dev, non_blocking=True).permute(0, 3, 1, 2).float() / 255
            yield normalize(artir(x) if self.egitim else test_goruntu(x)), self.y[idx.to(self.y.device)]


def model_kur(n):
    m = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
    m.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(m.classifier[1].in_features, n))
    return m


def calistir(model, veri, opt=None, crit=None, sched=None):
    """Bir tur eğitim (opt verilirse) ya da değerlendirme. fp32: bu GPU'da AMP iki kat yavaş ölçüldü."""
    egit = opt is not None
    model.train(egit)
    tum_logit, tum_y, kayip, n = [], [], 0.0, 0
    t0 = time.time()
    with torch.set_grad_enabled(egit):
        for adim, (x, y) in enumerate(veri, 1):
            out = model(x)
            loss = crit(out, y) if crit else F.cross_entropy(out, y)
            if egit:
                opt.zero_grad(set_to_none=True)
                loss.backward()
                opt.step()
                if sched:
                    sched.step()
                if adim % 50 == 0:
                    print(f"    adım {adim}/{len(veri)}  {time.time() - t0:.0f} sn", flush=True)
            kayip += loss.item() * len(y)
            n += len(y)
            tum_logit.append(out.detach().float().cpu())
            tum_y.append(y.cpu())
    return torch.cat(tum_logit), torch.cat(tum_y), kayip / max(1, n)


def topk(logits, y, k):
    return (logits.topk(k, 1).indices == y[:, None]).any(1).float().mean().item()


def sicaklik_bul(logits, y):
    """Doğrulama NLL'sini en aza indiren sıcaklık T (kalibrasyon)."""
    t = torch.ones(1, requires_grad=True)
    opt = torch.optim.LBFGS([t], lr=0.05, max_iter=200)

    def kapanis():
        opt.zero_grad()
        loss = F.cross_entropy(logits / t.clamp(min=0.05), y)
        loss.backward()
        return loss
    opt.step(kapanis)
    return float(t.clamp(min=0.05).item())


def ece(probs, y, bins=15):
    conf, pred = probs.max(1)
    dogru = pred.eq(y).float()
    e = torch.zeros(1)
    for lo in torch.linspace(0, 1, bins + 1)[:-1]:
        m = (conf > lo) & (conf <= lo + 1 / bins)
        if m.any():
            e += m.float().mean() * (conf[m].mean() - dogru[m].mean()).abs()
    return float(e)


def karar_vakasi(prob, classes):
    """model.js ile aynı dönüşüm: softmax -> {mantar_olma_olasiligi, simule_top5}."""
    neg = classes.index(NEG) if NEG in classes else -1
    p_not = float(prob[neg]) if neg >= 0 else 0.0
    tur = sorted(((c, float(prob[i]) / max(1e-9, 1 - p_not)) for i, c in enumerate(classes) if i != neg), key=lambda x: -x[1])
    return {"mantar_olma_olasiligi": 1 - p_not, "simule_top5": [{"latin_name": c, "p": p} for c, p in tur[:5]]}


def guvenlik_degerlendir(probs, y, classes, info, T):
    """Her test fotoğrafı için karar katmanının verdiği seviye; gerçek risk sınıfına göre tablo {risk: {karar: adet}}."""
    satirlar = []
    for p, yi in zip(probs, y):
        gercek = classes[yi]
        risk = "mantar_degil" if gercek == NEG else info[gercek]["risk"]
        satirlar.append((risk, decide(karar_vakasi(p.numpy(), classes), info, T)))
    tablo = {r: dict(Counter(k for rr, k in satirlar if rr == r)) for r in RISKLER if any(rr == r for rr, _ in satirlar)}

    def oran(riskler, karar):
        s = [k for r, k in satirlar if r in riskler]
        return float(np.mean([k == karar for k in s])) if s else None
    return tablo, {
        "tehlikeli_tur_kirmizi_orani": oran({"olumcul", "yuksek"}, "KIRMIZI"),
        "olumcul_tur_kirmizi_orani": oran({"olumcul"}, "KIRMIZI"),
        "tehlikeli_karisiklik_orani": oran({"olumcul", "yuksek"}, "GRI"),
        "tehlikeli_mantar_degil_orani": oran({"olumcul", "yuksek"}, "MANTAR_DEGIL"),
        "mantar_degil_dogru_red": oran({"mantar_degil"}, "MANTAR_DEGIL"),
        "dusuk_risk_gri_orani": oran({"dusuk"}, "GRI"),
    }


def grafikler(gecmis, cm, classes, tablo):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ep = [g["epoch"] for g in gecmis]
    ax[0].plot(ep, [g["train_loss"] for g in gecmis], label="train")
    ax[0].plot(ep, [g["val_loss"] for g in gecmis], label="val")
    ax[0].set_title("Kayıp"); ax[0].legend(); ax[0].set_xlabel("epoch")
    ax[1].plot(ep, [g["val_top1"] for g in gecmis], label="val top-1")
    ax[1].plot(ep, [g["val_top5"] for g in gecmis], label="val top-5")
    ax[1].set_title("Doğrulama doğruluğu"); ax[1].legend(); ax[1].set_xlabel("epoch")
    fig.tight_layout(); fig.savefig(OUT_RES / "egitim_egrileri.png", dpi=130); plt.close(fig)

    cmn = cm / cm.sum(1, keepdims=True).clip(min=1)
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(classes)), classes, rotation=90, fontsize=7)
    ax.set_yticks(range(len(classes)), classes, fontsize=7)
    ax.set_xlabel("Tahmin"); ax.set_ylabel("Gerçek"); ax.set_title("Karışıklık matrisi (test, satır normalize)")
    fig.tight_layout(); fig.savefig(OUT_RES / "karisiklik_matrisi.png", dpi=130); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 3.4))
    satir = list(tablo)
    t = np.array([[tablo[r].get(k, 0) for k in KARARLAR] for r in satir], dtype=float)
    t = t / t.sum(1, keepdims=True).clip(min=1)
    ax.imshow(t, cmap="Reds", vmin=0, vmax=1)
    ax.set_xticks(range(len(KARARLAR)), KARARLAR, fontsize=8); ax.set_yticks(range(len(satir)), satir)
    for i in range(t.shape[0]):
        for j in range(t.shape[1]):
            ax.text(j, i, f"{t[i, j]:.0%}", ha="center", va="center", fontsize=8)
    ax.set_title("Gerçek risk → uygulamanın kararı (test)")
    fig.tight_layout(); fig.savefig(OUT_RES / "guvenlik_matrisi.png", dpi=130); plt.close(fig)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=14)
    ap.add_argument("--head-epochs", type=int, default=3)
    ap.add_argument("--bs", type=int, default=64)
    a = ap.parse_args()
    torch.manual_seed(42)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Cihaz: {dev} {torch.cuda.get_device_name(0) if dev.type == 'cuda' else ''}", flush=True)

    with open(ROOT / "data" / "clean" / "inat_clean.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    siniflar = {r["sinif"] for r in rows}
    classes = sorted(siniflar - {NEG}) + ([NEG] if NEG in siniflar else [])
    tr, va, te = ([r for r in rows if r["split"] == s] for s in ("train", "val", "test"))
    print(f"{len(classes)} sınıf | train {len(tr)} · val {len(va)} · test {len(te)}", flush=True)
    X = onbellek(tr + va + te)
    y = [classes.index(r["sinif"]) for r in tr + va + te]
    a1, a2 = len(tr), len(tr) + len(va)
    dl_tr = GPUVeri(X[:a1], y[:a1], dev, a.bs, egitim=True)
    dl_va = GPUVeri(X[a1:a2], y[a1:a2], dev, a.bs, egitim=False)
    dl_te = GPUVeri(X[a2:], y[a2:], dev, a.bs, egitim=False)
    del X

    say = Counter(r["sinif"] for r in tr)
    w = torch.tensor([(len(tr) / (len(classes) * say[c])) ** 0.5 for c in classes], dtype=torch.float32)
    crit = nn.CrossEntropyLoss(weight=w.to(dev), label_smoothing=0.1)
    model = model_kur(len(classes)).to(dev)
    if dev.type == "cuda":
        # Windows sürücüsü GPU belleği dolunca hata vermeden sistem belleğine taşıyor ve eğitim ~100 kat yavaşlıyordu.
        # Üst sınır koyunca PyTorch önbelleğini boşaltır; cudnn.benchmark'ın büyük çalışma alanlı algoritmaları da kapalı.
        torch.cuda.set_per_process_memory_fraction(0.85)
        torch.backends.cudnn.benchmark = False
    gecmis, en_iyi, en_iyi_durum = [], -1.0, None

    def asama(epochs, params, lr, isim, ep0):
        nonlocal en_iyi, en_iyi_durum
        opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.02)
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=epochs * len(dl_tr), pct_start=0.15)
        for e in range(epochs):
            t0 = time.time()
            _, _, tl = calistir(model, dl_tr, opt, crit, sched)
            vl, vy, vloss = calistir(model, dl_va)
            g = {"epoch": ep0 + e + 1, "asama": isim, "train_loss": tl, "val_loss": vloss,
                 "val_top1": topk(vl, vy, 1), "val_top5": topk(vl, vy, 5)}
            gecmis.append(g)
            print(f"[{isim}] epoch {g['epoch']:>2}  train {tl:.3f}  val {vloss:.3f}  top1 {g['val_top1']:.3f}  "
                  f"top5 {g['val_top5']:.3f}  ({time.time() - t0:.0f}s"
                  + (f", GPU {torch.cuda.max_memory_reserved() / 2**30:.1f} GB)" if dev.type == "cuda" else ")"), flush=True)
            if g["val_top1"] > en_iyi:
                en_iyi, en_iyi_durum = g["val_top1"], {k: v.detach().clone() for k, v in model.state_dict().items()}

    for p in model.features.parameters():
        p.requires_grad = False
    asama(a.head_epochs, model.classifier.parameters(), 2e-3, "baş", 0)
    for p in model.features.parameters():
        p.requires_grad = True
    asama(a.epochs, model.parameters(), 4e-4, "tüm ağ", a.head_epochs)
    model.load_state_dict(en_iyi_durum)

    vl, vy, _ = calistir(model, dl_va)
    T_ = sicaklik_bul(vl, vy)
    tl_, ty, _ = calistir(model, dl_te)
    del dl_tr, dl_va, dl_te
    torch.cuda.empty_cache()
    p_ham, p_kal = F.softmax(tl_, 1), F.softmax(tl_ / T_, 1)
    pred = tl_.argmax(1)
    cm = np.zeros((len(classes), len(classes)), dtype=int)
    for g_, p_ in zip(ty.tolist(), pred.tolist()):
        cm[g_, p_] += 1
    recall = {c: float(cm[i, i] / max(1, cm[i].sum())) for i, c in enumerate(classes)}

    info = load()[1]
    T_esik = load()[0]["esikler"]
    tablo, guv = guvenlik_degerlendir(p_kal, ty, classes, info, T_esik)
    metrics = {
        "version": VERSION, "arch": "EfficientNet-B0", "classes": len(classes),
        "n_train": len(tr), "n_val": len(va), "n_test": len(te),
        "top1": topk(tl_, ty, 1), "top5": topk(tl_, ty, 5), "macro_recall": float(np.mean(list(recall.values()))),
        "temperature": T_, "ece_ham": ece(p_ham, ty), "ece_kalibre": ece(p_kal, ty),
        **guv, "sinif_recall": recall, "karar_tablosu": tablo, "gecmis": gecmis,
    }
    OUT_RES.mkdir(exist_ok=True)
    (OUT_RES / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=1), encoding="utf-8")
    grafikler(gecmis, cm, classes, tablo)

    # ---- ONNX dışa aktarma (cihazda çalışma için)
    OUT_MODEL.mkdir(parents=True, exist_ok=True)
    model.eval().float().cpu()
    torch.onnx.export(model, torch.randn(1, 3, SIZE, SIZE), OUT_MODEL / "mycoguard.onnx", input_names=["input"],
                      output_names=["logits"], opset_version=17, dynamo=False)
    (OUT_MODEL / "labels.json").write_text(json.dumps({
        "version": VERSION, "arch": "EfficientNet-B0", "classes": classes, "input_size": SIZE, "mean": MEAN, "std": STD,
        "temperature": T_, "metrics": {k: metrics[k] for k in ("top1", "top5", "macro_recall", "tehlikeli_tur_kirmizi_orani",
                                                                "tehlikeli_karisiklik_orani", "ece_kalibre")},
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- ONNX doğrulama: PyTorch ile aynı çıktı mı?
    import onnxruntime as ort
    x = torch.randn(2, 3, SIZE, SIZE)
    with torch.no_grad():
        ref = model(x).numpy()
    got = ort.InferenceSession(str(OUT_MODEL / "mycoguard.onnx")).run(None, {"input": x[:1].numpy()})[0]
    fark = float(np.abs(ref[:1] - got).max())
    print(f"ONNX doğrulama: en büyük fark {fark:.2e}", flush=True)

    rapor(metrics, classes, tablo, fark)
    print(f"\nTest: top-1 {metrics['top1']:.3f} · top-5 {metrics['top5']:.3f} · tehlikeli→KIRMIZI "
          f"{guv['tehlikeli_tur_kirmizi_orani']:.3f} · tehlikeli karışıklık {guv['tehlikeli_karisiklik_orani']:.3f}", flush=True)


def rapor(m, classes, tablo, fark):
    info = load()[1]
    L = ["# Model eğitim raporu", "",
         f"**Model:** {m['arch']} (ImageNet ön eğitimli, transfer öğrenme) · **{m['classes']} sınıf** · "
         f"train {m['n_train']} / val {m['n_val']} / test {m['n_test']} fotoğraf", "",
         "## Genel başarı (test seti — eğitimde hiç görülmedi)", "", "| Metrik | Değer |", "|---|---:|",
         f"| Top-1 doğruluk | {m['top1']:.1%} |", f"| Top-5 doğruluk | {m['top5']:.1%} |",
         f"| Makro recall | {m['macro_recall']:.1%} |",
         f"| Kalibrasyon hatası (ECE) ham → kalibre | {m['ece_ham']:.3f} → {m['ece_kalibre']:.3f} (T={m['temperature']:.2f}) |",
         "", "## Güvenlik metrikleri (model + karar katmanı birlikte)", "", "| Metrik | Değer | Hedef |", "|---|---:|---|",
         f"| Ölümcül/zehirli tür fotoğrafının KIRMIZI gösterilme oranı | {m['tehlikeli_tur_kirmizi_orani']:.1%} | yüksek |",
         f"| Ölümcül tür fotoğrafının KIRMIZI gösterilme oranı | {(m['olumcul_tur_kirmizi_orani'] or 0):.1%} | yüksek |",
         f"| **Tehlikeli karışıklık** (zehirli → 'düşük riskli aday') | **{m['tehlikeli_karisiklik_orani']:.1%}** | ≈ 0 |",
         f"| Zehirli tür fotoğrafının 'mantar değil' sayılması | {m['tehlikeli_mantar_degil_orani']:.1%} | ≈ 0 |",
         f"| Mantar olmayan fotoğrafların reddedilmesi | {m['mantar_degil_dogru_red']:.1%} | yüksek |",
         f"| Düşük riskli türlerde GRİ sonuç (gereksiz alarm olmaması) | {m['dusuk_risk_gri_orani']:.1%} | — |",
         "", "### Gerçek risk → uygulamanın kararı (adet)", "",
         "| Gerçek risk | " + " | ".join(KARARLAR) + " |", "|---|" + "---:|" * len(KARARLAR),
         *[f"| {r} | " + " | ".join(str(tablo[r].get(k, 0)) for k in KARARLAR) + " |" for r in tablo], "",
         "![güvenlik](guvenlik_matrisi.png)", "", "## Sınıf bazında recall (test)", "", "| Sınıf | Risk | Recall |", "|---|---|---:|"]
    for c in classes:
        L.append(f"| *{c}* | {info[c]['risk'] if c in info else '—'} | {m['sinif_recall'][c]:.1%} |")
    L += ["", "![eğriler](egitim_egrileri.png)", "", "![karışıklık](karisiklik_matrisi.png)", "",
          f"ONNX dışa aktarma doğrulaması: PyTorch ile en büyük çıktı farkı {fark:.2e}.", ""]
    (OUT_RES / "egitim_raporu.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
