"""Gemma 4 (Ollama) ile görsel özellik analizi ve bilgi tabanına dayalı soru-cevap.

Güvenlik tasarımı:
  * Gemma'dan serbest metin "yenir/yenmez" kararı istenmez. Önce YAPILANDIRILMIŞ görsel
    özellikler (JSON) istenir; risk kararını kural katmanı verir.
  * Gemma'nın bulguları riski yalnızca YÜKSELTEBİLİR (ör. sap tabanında torba görülürse
    ölümcül Amanita uyarısı), hiçbir zaman düşüremez.
  * Sohbet yanıtları yalnızca species_info.csv bilgisine dayanır (RAG) ve sistem talimatı
    "yenilebilir/güvenli" demeyi yasaklar; çıktı ayrıca süzgeçten geçirilir.
"""
import json
import os
import re
import urllib.error
import urllib.request

OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.environ.get("MYCOGUARD_GEMMA", "gemma4:e4b")

OZELLIK_SEMASI = {
    "type": "object",
    "properties": {
        "mantar_mi": {"type": "boolean"},
        "alt_yuz": {"type": "string", "enum": ["lamel", "gozenek", "diken", "damar", "petek", "gorunmuyor"]},
        "lamel_rengi": {"type": "string", "enum": ["beyaz", "krem", "sari", "pembe", "kahverengi", "siyah", "diger", "gorunmuyor"]},
        "sapta_halka": {"type": "string", "enum": ["var", "yok", "gorunmuyor"]},
        "sap_tabaninda_torba": {"type": "string", "enum": ["var", "yok", "gorunmuyor"]},
        "sapka_rengi": {"type": "string"},
        "sapka_ustunde_sigil_pul": {"type": "string", "enum": ["var", "yok", "gorunmuyor"]},
        "yetistigi_yer": {"type": "string", "enum": ["toprak", "odun", "cim", "gorunmuyor"]},
        "kumeler_halinde": {"type": "string", "enum": ["evet", "hayir", "gorunmuyor"]},
        "foto_kalitesi": {"type": "string", "enum": ["iyi", "orta", "kotu"]},
        "eksik_acilar": {"type": "array", "items": {"type": "string"}},
        "aciklama": {"type": "string"},
    },
    "required": ["mantar_mi", "alt_yuz", "lamel_rengi", "sapta_halka", "sap_tabaninda_torba", "yetistigi_yer",
                 "foto_kalitesi", "eksik_acilar", "aciklama"],
}

SISTEM = (
    "Sen MycoGuard Kastamonu'nun mantar güvenliği asistanısın. Türkçe, kısa ve net yaz. "
    "KESİN KURALLAR: (1) Hiçbir mantar için 'yenilebilir', 'güvenli', 'zehirsiz', 'yiyebilirsin' deme; yeme kararı "
    "her zaman uzman onayı gerektirir. (2) Yalnızca sana verilen BİLGİ TABANI metnine dayan; orada olmayan tür "
    "bilgisini uydurma, 'bilgi tabanımda yok' de. (3) Biri mantar yediğini söylerse önce 112 / 114'ü aramasını, "
    "belirti beklememesini ve mantar örneğini saklamasını söyle. (4) Tıbbi teşhis koyma."
)

YASAK = re.compile(r"\b(yenilebilir|yenebilir|güvenle yiye|güvenlidir|zehirsizdir|yiyebilirsin|yiyebilirsiniz)\b", re.I)


def _post(path, body, timeout=300):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def durum():
    """Ollama çalışıyor mu, model yüklü mü?"""
    try:
        with urllib.request.urlopen(OLLAMA + "/api/tags", timeout=3) as r:
            adlar = [m["name"] for m in json.load(r).get("models", [])]
        return {"ollama": True, "model": MODEL, "hazir": any(a == MODEL or a.startswith(MODEL + ":") for a in adlar)}
    except (urllib.error.URLError, OSError, ValueError):
        return {"ollama": False, "model": MODEL, "hazir": False}


def gorsel_ozellikler(image_b64):
    """Fotoğraftan yapılandırılmış ayırt edici özellikleri çıkarır."""
    prompt = (
        "Bu fotoğraftaki mantarın YALNIZCA görünen özelliklerini şemaya göre doldur. Emin olmadığın veya fotoğrafta "
        "görünmeyen her şey için 'gorunmuyor' yaz; tahmin etme. 'eksik_acilar' alanına güvenli tanı için çekilmesi "
        "gereken eksik fotoğrafları yaz (ör. 'şapka altı', 'sap tabanı (toprağı kazıyarak)', 'boyuna kesit'). "
        "'aciklama' alanına gördüklerini 1-2 Türkçe cümleyle yaz; tür adı veya yenebilirlik yorumu yapma."
    )
    r = _post("/api/chat", {
        "model": MODEL, "stream": False, "format": OZELLIK_SEMASI, "options": {"temperature": 0},
        "messages": [{"role": "user", "content": prompt, "images": [image_b64]}],
    })
    return json.loads(r["message"]["content"])


def risk_yukseltme(oz, info, aday_adlari):
    """Gemma bulgularından kural tabanlı ek uyarılar. Riski sadece yükseltir; KIRMIZI'ya çekebilir."""
    uyarilar, kirmizi = [], False
    torba, halka, lamel = oz.get("sap_tabaninda_torba"), oz.get("sapta_halka"), oz.get("lamel_rengi")
    if torba == "var":
        kirmizi = True
        uyarilar.append("Sap tabanında torba (volva) görünüyor. Bu, ölümcül köygöçüren grubunun (Amanita) en önemli işaretidir.")
    if lamel == "beyaz" and halka == "var" and oz.get("alt_yuz") == "lamel":
        kirmizi = True
        uyarilar.append("Beyaz lamel + sapta halka: ölümcül beyaz Amanita türleriyle (köygöçüren, ak köygöçüren) uyumlu bir özellik bileşimi.")
    if oz.get("yetistigi_yer") == "odun" and oz.get("kumeler_halinde") == "evet" and \
            any(info.get(a, {}).get("risk") == "dusuk" for a in aday_adlari[:1]):
        uyarilar.append("Odun üzerinde kümeler halinde: ölümcül galerina, zeytin mantarı ve kükürt mantarı da böyle büyür.")
    if oz.get("alt_yuz") == "petek":
        uyarilar.append("Petekli şapka: kuzugöbeği / sahte kuzugöbeği ayrımı için mantarı boyuna kesip içinin tamamen boş olduğunu kontrol edin.")
    if torba == "gorunmuyor" and oz.get("alt_yuz") in ("lamel", "gorunmuyor"):
        uyarilar.append("Sap tabanı görünmüyor: mantarı toprağı kazıyarak çıkarıp sap tabanını da fotoğraflayın.")
    if oz.get("foto_kalitesi") == "kotu":
        uyarilar.append("Fotoğraf kalitesi düşük; daha net ve yakın bir fotoğraf çekin.")
    return {"kirmiziya_cek": kirmizi, "uyarilar": uyarilar}


def bilgi_tabani(info, adlar):
    alanlar = ["turkce_ad", "risk", "zehir_notu", "belirtiler", "belirti_baslangici", "ilk_yardim_notu", "habitat",
               "kastamonu_notu", "sapka_cm", "sap_cm", "yetisme_sureci", "mevsim", "toplama_notu", "ikiz_turler",
               "ayirt_edici_ipucu"]
    return "\n\n".join(f"### {a}\n" + "\n".join(f"- {k}: {info[a][k]}" for k in alanlar) for a in adlar if a in info)


def ilgili_turler(info, soru, baglam_adlari, n=6):
    """Basit anahtar kelime eşleşmesiyle (RAG) soruyla ilgili türleri seçer."""
    s = soru.lower()
    puan = {}
    for a, r in info.items():
        metin = f"{a} {r['turkce_ad']} {r['yerel_ad']}".lower()
        puan[a] = sum(3 for k in re.split(r"[\s;(),]+", metin) if len(k) > 3 and k in s)
    secilen = list(dict.fromkeys(baglam_adlari + [a for a, p in sorted(puan.items(), key=lambda x: -x[1]) if p > 0]))
    return secilen[:n]


def sohbet(info, mesajlar, baglam):
    """mesajlar: [{role, content}], baglam: {seviye, adaylar:[ad], ozellikler}"""
    soru = mesajlar[-1]["content"]
    adlar = ilgili_turler(info, soru, baglam.get("adaylar", []))
    sistem = SISTEM + "\n\nBİLGİ TABANI (yalnızca buna dayan):\n" + bilgi_tabani(info, adlar)
    if baglam.get("seviye"):
        sistem += (f"\n\nSON ANALİZ: risk seviyesi {baglam['seviye']}; adaylar: {', '.join(baglam.get('adaylar', []))}; "
                   f"görsel bulgular: {json.dumps(baglam.get('ozellikler') or {}, ensure_ascii=False)}. "
                   "Risk seviyesini asla düşük gösterme.")
    r = _post("/api/chat", {"model": MODEL, "stream": False, "options": {"temperature": 0.2},
                            "messages": [{"role": "system", "content": sistem}] + mesajlar[-8:]})
    cevap = r["message"]["content"].strip()
    if YASAK.search(cevap):
        cevap = YASAK.sub("[uzman onayı gerekir]", cevap)
        cevap += "\n\n⚠️ Hatırlatma: MycoGuard hiçbir mantarın yenilebilir olduğunu söylemez; yeme kararı için uzman onayı şarttır."
    return {"cevap": cevap, "kaynak_turler": adlar}
