"""Gemma 4 (uzak API) ile görsel özellik analizi ve bilgi tabanına dayalı soru-cevap.

Sağlayıcılar (ortam değişkeni MYCOGUARD_LLM):
  * gemini  (varsayılan) — Google Gemini API üzerinden Gemma 4, GEMINI_API_KEY gerekir
  * openai  — OpenAI uyumlu herhangi bir uç: DigitalOcean Gradient, Hugging Face, vLLM, Ollama…
              OPENAI_BASE_URL + OPENAI_API_KEY
Model adı: MYCOGUARD_MODEL (varsayılan gemma-4-26b-a4b-it)

Güvenlik tasarımı:
  * Gemma'dan serbest "yenir/yenmez" kararı istenmez; YAPILANDIRILMIŞ görsel özellikler (JSON)
    istenir ve şemaya uymayan her değer "gorunmuyor" kabul edilir. Risk kararını kural katmanı verir.
  * Gemma bulguları riski yalnızca YÜKSELTEBİLİR, asla düşüremez.
  * Sohbet yanıtları yalnızca species_info.csv bilgisine dayanır (RAG); çıktı süzgeçten geçer.
"""
import json
import os
import re
import urllib.error
import urllib.request
from datetime import date

SAGLAYICI = os.environ.get("MYCOGUARD_LLM", "gemini").lower()
MODEL = os.environ.get("MYCOGUARD_MODEL", "gemma-4-26b-a4b-it")
GEMINI_URL = os.environ.get("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
OPENAI_URL = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
# Gemma 4 yanıt öncesi "düşünme" yapar; "minimal" iki fotoğraflı analizi ~180 sn'den ~5 sn'ye indirir
# ve ölçümlerde aynı özellikleri buldu. Boş bırakılırsa modelin varsayılanı kullanılır.
DUSUNME = os.environ.get("MYCOGUARD_THINKING", "minimal")

ENUMLAR = {
    "alt_yuz": ["lamel", "gozenek", "diken", "damar", "petek", "gorunmuyor"],
    "lamel_rengi": ["beyaz", "krem", "sari", "pembe", "kahverengi", "siyah", "diger", "gorunmuyor"],
    "sapta_halka": ["var", "yok", "gorunmuyor"],
    "sap_tabaninda_torba": ["var", "yok", "gorunmuyor"],
    "sapka_ustunde_sigil_pul": ["var", "yok", "gorunmuyor"],
    "yetistigi_yer": ["toprak", "odun", "cim", "gorunmuyor"],
    "kumeler_halinde": ["evet", "hayir", "gorunmuyor"],
    "foto_kalitesi": ["iyi", "orta", "kotu"],
}

SISTEM = (
    "Sen MycoGuard Kastamonu'nun mantar güvenliği asistanısın. Kastamonu ve Batı Karadeniz ormanlarındaki mantarlar "
    "hakkında Türkçe, yardımsever ve doyurucu yanıtlar ver.\n"
    "YANIT BİÇİMİ: Tek cümlelik bir girişle başla; ardından madde işaretli (- ) ayrıntılar ver (gerektiği kadar, "
    "genellikle 4-10 madde). Türleri Türkçe adı ve parantez içinde Latince adıyla an, önemli kelimeleri **kalın** yaz. "
    "Uygun olduğunda risk seviyesi, belirtilerin kaç saatte başladığı, ayırt edici özellikler, yetiştiği yer ve "
    "görüldüğü aylar gibi bilgileri ekle. Liste istenirse TÜR KATALOĞU'ndaki türleri risk gruplarına göre listele. "
    "Sonunda tek cümlelik güvenlik hatırlatması ve gerekiyorsa bir sonraki adım önerisi yaz.\n"
    "KESİN KURALLAR: (1) Hiçbir mantar için 'yenilebilir', 'güvenli', 'zehirsiz', 'yiyebilirsin' deme; yeme kararı "
    "her zaman uzman onayı gerektirir. (2) Yalnızca TÜR KATALOĞU ve BİLGİ TABANI metnine dayan; orada olmayan tür "
    "bilgisini uydurma, rehberde olmadığını söyle. (3) Biri mantar yediğini söylerse önce 112 / 114'ü aramasını, "
    "belirti beklememesini ve mantar örneğini saklamasını söyle. (4) Tıbbi teşhis koyma."
)
AY_ADLARI = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
RISK_ADI = {"olumcul": "ölümcül", "yuksek": "zehirli", "orta": "şartlı risk", "dusuk": "düşük risk"}

YASAK = re.compile(r"\b(yenilebilir|yenebilir|güvenle yiye|güvenlidir|zehirsizdir|yiyebilirsin|yiyebilirsiniz)\b", re.I)


class LLMHatasi(Exception):
    pass


def _anahtar():
    return os.environ.get("GEMINI_API_KEY" if SAGLAYICI == "gemini" else "OPENAI_API_KEY", "")


def _post(url, body, headers=None, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise LLMHatasi(f"{SAGLAYICI} API hatası {e.code}: {e.read()[:300].decode(errors='replace')}") from e
    except OSError as e:
        raise LLMHatasi(f"{SAGLAYICI} API'ye ulaşılamadı: {e}") from e


def uret(mesajlar, images=(), temperature=0.2):
    """mesajlar: [{role: system|user|assistant, content}] -> model yanıt metni.
    images (base64 JPEG listesi) verilirse son kullanıcı mesajına eklenir."""
    if not _anahtar():
        raise LLMHatasi("API anahtarı tanımlı değil")
    sistem = "\n\n".join(m["content"] for m in mesajlar if m["role"] == "system")
    diyalog = [m for m in mesajlar if m["role"] != "system"]

    if SAGLAYICI == "gemini":
        contents = []
        for i, m in enumerate(diyalog):
            metin = (sistem + "\n\n" + m["content"]) if i == 0 and sistem else m["content"]
            parts = [{"text": metin}]
            if i == len(diyalog) - 1:
                parts += [{"inline_data": {"mime_type": "image/jpeg", "data": b}} for b in images]
            contents.append({"role": "model" if m["role"] == "assistant" else "user", "parts": parts})
        cfg = {"temperature": temperature}
        if DUSUNME:
            cfg["thinkingConfig"] = {"thinkingLevel": DUSUNME}
        r = _post(f"{GEMINI_URL}/models/{MODEL}:generateContent", {"contents": contents, "generationConfig": cfg},
                  {"x-goog-api-key": _anahtar()})
        try:
            parts = r["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError) as e:
            raise LLMHatasi(f"Beklenmeyen yanıt: {json.dumps(r)[:300]}") from e
        # Düşünme (thought) parçalarını atla, yalnızca yanıt metnini al
        return "".join(p.get("text", "") for p in parts if not p.get("thought")).strip()

    if not OPENAI_URL:
        raise LLMHatasi("OPENAI_BASE_URL tanımlı değil")
    msgs = ([{"role": "system", "content": sistem}] if sistem else []) + [dict(m) for m in diyalog]
    if images:
        msgs[-1]["content"] = [{"type": "text", "text": msgs[-1]["content"]}] + \
            [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b}"}} for b in images]
    r = _post(f"{OPENAI_URL}/chat/completions", {"model": MODEL, "messages": msgs, "temperature": temperature},
              {"Authorization": f"Bearer {_anahtar()}"})
    try:
        return r["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise LLMHatasi(f"Beklenmeyen yanıt: {json.dumps(r)[:300]}") from e


def durum():
    return {"saglayici": SAGLAYICI, "model": MODEL, "hazir": bool(_anahtar()) and (SAGLAYICI == "gemini" or bool(OPENAI_URL))}


# ------------------------------------------------------------------ görsel özellikler
def json_cikar(metin):
    """Model yanıtındaki ilk JSON nesnesini çıkarır (```json bloklarına ve önsöze dayanıklı)."""
    m = re.search(r"\{.*\}", metin or "", re.S)
    if not m:
        raise LLMHatasi("Yanıtta JSON bulunamadı")
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        raise LLMHatasi(f"JSON çözülemedi: {e}") from e


def ozellik_dogrula(ham):
    """Şemaya uymayan her değeri güvenli varsayılana çeker ('gorunmuyor' / kötü kalite)."""
    oz = {}
    for k, izinli in ENUMLAR.items():
        v = str(ham.get(k, "")).strip().lower()
        oz[k] = v if v in izinli else ("orta" if k == "foto_kalitesi" else "gorunmuyor")
    oz["mantar_mi"] = ham.get("mantar_mi") is not False
    oz["sapka_rengi"] = str(ham.get("sapka_rengi", ""))[:40]
    oz["eksik_acilar"] = [str(x)[:60] for x in ham.get("eksik_acilar", []) if x][:4] if isinstance(ham.get("eksik_acilar"), list) else []
    oz["aciklama"] = YASAK.sub("", str(ham.get("aciklama", "")))[:300]
    return oz


def gorsel_ozellikler(images):
    """images: aynı mantarın 1-3 fotoğrafı (base64 JPEG). Tek istekte birlikte değerlendirilir."""
    images = list(images)[:3]
    alanlar = "\n".join(f'  "{k}": {" | ".join(repr(x) for x in v)}' for k, v in ENUMLAR.items())
    giris = ("Bu fotoğraftaki mantarın" if len(images) == 1 else
             f"Bu {len(images)} fotoğraf AYNI mantarın farklı açılarıdır (ör. şapka üstü, şapka altı, sap tabanı). Hepsini birlikte değerlendirip mantarın")
    prompt = (
        f"{giris} YALNIZCA görünen özelliklerini çıkar. Emin olmadığın veya fotoğraflarda görünmeyen her "
        "şey için 'gorunmuyor' yaz; tahmin etme. Tür adı veya yenebilirlik yorumu YAPMA.\n"
        "Yalnızca şu JSON nesnesini döndür, başka metin yazma:\n{\n"
        '  "mantar_mi": true | false,\n' + alanlar + ',\n'
        '  "sapka_rengi": "kısa Türkçe renk",\n'
        '  "eksik_acilar": ["güvenli tanı için çekilmesi gereken eksik fotoğraflar, ör. şapka altı, sap tabanı (toprağı kazıyarak), boyuna kesit"],\n'
        '  "aciklama": "gördüklerinin 1-2 cümlelik Türkçe özeti"\n}'
    )
    return ozellik_dogrula(json_cikar(uret([{"role": "user", "content": prompt}], images=images, temperature=0)))


def risk_yukseltme(oz, info=None, aday_adlari=()):
    """Gemma bulgularından kural tabanlı ek uyarılar. Riski sadece yükseltir; KIRMIZI'ya çekebilir.
    Görüntü modeliyle paralel çalıştığı için aday türlerine bağlı değildir."""
    uyarilar, kirmizi = [], False
    torba, halka, lamel = oz.get("sap_tabaninda_torba"), oz.get("sapta_halka"), oz.get("lamel_rengi")
    if torba == "var":
        kirmizi = True
        uyarilar.append("Sap tabanında torba (volva) görünüyor. Bu, ölümcül köygöçüren grubunun (Amanita) en önemli işaretidir.")
    if lamel == "beyaz" and halka == "var" and oz.get("alt_yuz") == "lamel":
        kirmizi = True
        uyarilar.append("Beyaz lamel + sapta halka: ölümcül köygöçüren ile uyumlu bir özellik bileşimi.")
    if oz.get("yetistigi_yer") == "odun" and oz.get("kumeler_halinde") == "evet":
        uyarilar.append("Odun üzerinde kümeler halinde: ölümcül galerina, zeytin mantarı ve kükürt mantarı da böyle büyür.")
    if oz.get("alt_yuz") == "petek":
        uyarilar.append("Petekli şapka: kuzugöbeği / sahte kuzugöbeği ayrımı için mantarı boyuna kesip içinin tamamen boş olduğunu kontrol edin.")
    if torba == "gorunmuyor" and oz.get("alt_yuz") in ("lamel", "gorunmuyor"):
        uyarilar.append("Sap tabanı görünmüyor: mantarı toprağı kazıyarak çıkarıp sap tabanını da fotoğraflayın.")
    if oz.get("foto_kalitesi") == "kotu":
        uyarilar.append("Fotoğraf kalitesi düşük; daha net ve yakın bir fotoğraf çekin.")
    return {"kirmiziya_cek": kirmizi, "uyarilar": uyarilar}


# ------------------------------------------------------------------ sohbet (RAG)
def bilgi_tabani(info, adlar):
    alanlar = ["turkce_ad", "risk", "zehir_notu", "belirtiler", "belirti_baslangici", "ilk_yardim_notu", "habitat",
               "kastamonu_notu", "sapka_cm", "sap_cm", "yetisme_sureci", "mevsim", "toplama_notu", "ikiz_turler",
               "ayirt_edici_ipucu"]
    return "\n\n".join(f"### {a}\n" + "\n".join(f"- {k}: {info[a][k]}" for k in alanlar) for a in adlar if a in info)


def katalog(info):
    """Rehberdeki tüm türlerin kısa özeti: liste, ay ve risk sorularının hepsine yanıt verebilmek için."""
    satirlar = []
    for r in sorted(info.values(), key=lambda r: ["olumcul", "yuksek", "orta", "dusuk"].index(r["risk"])):
        aylar = ", ".join(AY_ADLARI[int(a) - 1] for a in r["aylar"].split(";") if a)
        yerel = f"; yöresel adı: {r['yerel_ad']}" if r["yerel_ad"] not in ("", "—") else ""
        satirlar.append(f"- {r['turkce_ad']} ({r['latin_name']}) — {RISK_ADI[r['risk']]}{yerel}; görüldüğü aylar: {aylar}; "
                        f"belirti başlangıcı: {r['belirti_baslangici']}; yetiştiği yer: {r['habitat']}")
    return "\n".join(satirlar)


GENEL_KELIMELER = {"mantarı", "mantar", "mantari", "zehirli", "yeşil", "kırmızı", "beyaz", "siyah", "sahte", "benekli"}


def ilgili_turler(info, soru, baglam_adlari, n=6):
    """Basit anahtar kelime eşleşmesiyle (RAG) soruyla ilgili türleri seçer.
    'mantarı' gibi her türün adında geçen genel kelimeler eşleşme sayılmaz."""
    kelimeler = re.findall(r"\w+", soru.lower())
    puan = {}
    for a, r in info.items():
        metin = f"{a} {r['turkce_ad']} {r['yerel_ad']}".lower()
        # Türkçe ekler için önek eşleşmesi: "köygöçüren" ~ "köygöçüreni"; kısa kelimeler ("sarı") yanlış eşleşmesin diye ≥5 harf
        puan[a] = sum(3 for k in set(re.split(r"[\s;(),]+", metin))
                      if len(k) >= 5 and k not in GENEL_KELIMELER and any(w.startswith(k) for w in kelimeler))
    secilen = list(dict.fromkeys(baglam_adlari + [a for a, p in sorted(puan.items(), key=lambda x: -x[1]) if p > 0]))
    return secilen[:n]


def sohbet(info, mesajlar, baglam):
    """mesajlar: [{role, content}], baglam: {seviye, adaylar:[ad], ozellikler}"""
    mesajlar = [{"role": m["role"] if m.get("role") in ("user", "assistant") else "user", "content": str(m.get("content", ""))[:2000]}
                for m in mesajlar[-8:]]
    adlar = ilgili_turler(info, mesajlar[-1]["content"], baglam.get("adaylar", []))
    sistem = (SISTEM + f"\n\nBugün: {AY_ADLARI[date.today().month - 1]} ayı.\n\nTÜR KATALOĞU (rehberdeki {len(info)} türün tamamı):\n"
              + katalog(info) + "\n\nBİLGİ TABANI (soruyla ilgili türlerin ayrıntıları):\n" + (bilgi_tabani(info, adlar) or "—"))
    if baglam.get("seviye"):
        sistem += (f"\n\nSON ANALİZ: risk seviyesi {baglam['seviye']}; adaylar: {', '.join(baglam.get('adaylar', []))}; "
                   f"görsel bulgular: {json.dumps(baglam.get('ozellikler') or {}, ensure_ascii=False)}. "
                   "Risk seviyesini asla düşük gösterme.")
    cevap = uret([{"role": "system", "content": sistem}] + mesajlar)
    if YASAK.search(cevap):
        cevap = YASAK.sub("[uzman onayı gerekir]", cevap)
        cevap += "\n\n⚠️ Hatırlatma: MycoGuard hiçbir mantarın yenilebilir olduğunu söylemez; yeme kararı için uzman onayı şarttır."
    return {"cevap": cevap, "kaynak_turler": adlar}
