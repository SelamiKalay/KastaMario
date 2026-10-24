# Telefona aktarma ve yayımlama

## Mimari

```
Telefon (Android / iOS — Capacitor)                Sunucu (DigitalOcean App Platform)
├─ EfficientNet-B0 (ONNX, onnxruntime-web)          server/app.py
│    fotoğraf → tür olasılıkları  [internetsiz]        ├─ /api/analiz  → Gemma 4 görsel özellikler
├─ Güvenlik kuralları (decide.js)  [internetsiz]       ├─ /api/sohbet  → Gemma 4 asistan (RAG)
├─ Rehber, Takvim, Yedim! (data.js) [internetsiz]      └─ API anahtarı yalnızca burada (ortam değişkeni)
└─ Gemma analizi + Asistan ── HTTPS ──────────────────────► Gemini API (Gemma 4, gemma-4-26b-a4b-it)
```

| Özellik | İnternet gerekir mi? | Nerede çalışır |
|---|---|---|
| Fotoğraftan tür tahmini + risk seviyesi | Hayır | Telefonda (ONNX) |
| Rehber, takvim, belirti zaman çizelgesi, 114/112 | Hayır | Telefonda |
| Gemma 4 görsel özellik analizi (torba, halka, lamel…) | Evet | Sunucu → Gemini API |
| Gemma 4 asistan | Evet | Sunucu → Gemini API |

İnternet yoksa uygulama görüntü modeli + güvenlik kurallarıyla çalışmaya devam eder; Gemma adımı "kullanılamıyor" görünür ve risk asla düşürülmez. Ormanda kapsama alanı dışında olmak yaygın olduğundan çekirdek özellikler bilerek cihazda tutuldu.

**API anahtarı uygulamanın içine konmaz.** APK içindeki her şey çözümlenebilir; anahtar yalnızca sunucuda ortam değişkenidir. Sunucu IP başına istek sınırı uygular (`MYCOGUARD_RATE`, varsayılan 10 dakikada 30).

## Hızlı test: telefondan https bağlantısı (Cloudflare Tunnel, hesap gerekmez)
Bilgisayarda sunucu çalışırken herkese açık, geçici bir `https` adresi verir; telefon mobil veride bile açabilir ve uygulamayı ana ekrana **kurabilir** (PWA, https gerektirir).

1. Sunucuyu başlatın: `python server/app.py` (anahtar `.env` dosyasından okunur)
2. [cloudflared](https://github.com/cloudflare/cloudflared/releases)'ı indirin (Cloudflare imzalı) ve çalıştırın:
   `cloudflared tunnel --no-autoupdate --url http://localhost:8000`
3. Çıktıdaki `https://….trycloudflare.com` adresini telefonda açın → menüden **Ana ekrana ekle / Uygulamayı yükle**.

Notlar: Adres tünel her başlatıldığında değişir ve yalnızca bilgisayar açıkken çalışır. Bağlantıyı bilen herkes uygulamayı kullanabilir; Gemma uçları IP başına istek sınırıyla korunur (`MYCOGUARD_RATE`). Kalıcı adres için DigitalOcean'a yayımlayın (aşağıda).

Aynı Wi-Fi'da tünelsiz test: telefonda `http://<bilgisayarın-yerel-IP'si>:8000` (ör. `ipconfig` → IPv4). Bu durumda uygulama kurulamaz, tarayıcıda çalışır.

## 1. Gemini API anahtarı
1. https://aistudio.google.com/apikey adresinden anahtar oluşturun (Gemma 4 ücretsiz katmanda sunulur; ücretsiz katmanda gönderilen veriler Google ürünlerini geliştirmek için kullanılabilir).
2. Yerelde deneme: `GEMINI_API_KEY=... python server/app.py` → http://localhost:8000

## 2. Sunucuyu yayımlama (DigitalOcean App Platform)
1. Repo GitHub'da public olmalı (`SelamiKalay/BAKLAVA`).
2. DigitalOcean → Apps → Create App → GitHub reposunu seçin; ya da `doctl apps create --spec .do/app.yaml`.
3. Ortam değişkenleri: `GEMINI_API_KEY` (Encrypted). Diğerleri `.do/app.yaml` içinde.
4. Yayımlanan adresi (ör. `https://mycoguard-xxxx.ondigitalocean.app/`) not edin.

Alternatif sağlayıcı (OpenAI uyumlu; ör. DigitalOcean Serverless Inference, Hugging Face, vLLM):
`MYCOGUARD_LLM=openai OPENAI_BASE_URL=https://... OPENAI_API_KEY=... MYCOGUARD_MODEL=<model-id>`

## 3. Android uygulaması (Capacitor)
Gereksinimler: Node.js, Android Studio (Android SDK).

```bash
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap add android
```

1. `app/config.js` içinde `window.MYCO_API` değerini yayımlanan sunucu adresi yapın.
2. `npx cap sync android` → `npx cap open android` → Android Studio'da **Run** ya da **Build > Build APK**.
3. Kamera izni: `capture="environment"` dosya seçici Android'de kamerayı açar; ek eklenti gerekmez.

iOS için aynı adımlar `@capacitor/ios` ile (Xcode gerekir).

## 4. PWA olarak (en hızlı yol)
Sunucu yayımlandıktan sonra adresi telefonda Chrome/Safari ile açıp **Ana ekrana ekle** deyin. Uygulama tam ekran açılır ve servis çalışanı sayesinde çevrimdışı da çalışır.

## Gelecek: Gemma 4 tamamen cihazda
Gemma 4 E2B, LiteRT-LM biçiminde (~2,4 GB, INT4) Android'de çalıştırılabiliyor. Bu, asistanı internetsiz yapabilir; ancak uygulama boyutu ve orta segment telefonlarda hız nedeniyle şimdilik sunucu tercih edildi.
