# 🍄 KastaMario — Kastamonu mushroom guide

[Türkçe](README.tr.md) · **English**

<img src="app/img/kastamario.png" alt="KastaMario logo" width="120" align="right">

**An AI-powered mushroom poisoning risk guide.** Take a photo of a mushroom and KastaMario shows the likely species, the poisoning risk, deadly look-alikes, how many hours until symptoms start, what to do if you ate it, and where and when the mushroom grows. It is built for the forests of Kastamonu, Türkiye (Küre Mountains, Ilgaz, coastal chestnut–oak forests).

> KastaMario **never says a mushroom is edible.** Mistaking a poisonous mushroom for an edible one can kill; mistaking an edible one for poisonous costs, at most, an empty basket. This asymmetry is the foundation of the design.

**Why now:** in October 2026 more than 40 people in Kastamonu went to hospital with mushroom poisoning in a single week, and in neighbouring Sinop 76 people sought treatment between 1 September and 14 October. Experts warn there is no way to tell a poisonous mushroom at home, and folk tests (silver spoon, vinegar, cooking with onion) do not work.

| Scan | Guide | Calendar | I ate it! |
|:---:|:---:|:---:|:---:|
| <img src="docs/img/tara.jpg" width="200" alt="Scan screen: Gemma 4 findings on the anatomy photo"> | <img src="docs/img/rehber.png" width="200" alt="Guide screen"> | <img src="docs/img/takvim.png" width="200" alt="Calendar screen"> | <img src="docs/img/acil.png" width="200" alt="Emergency screen"> |

*The app interface is in Turkish, for its local users.*

## What does the AI do?

KastaMario combines two open models with a rule-based safety layer:

| Layer | Model | License | Role |
|---|---|---|---|
| 1. Image classifier | **EfficientNet-B0**, trained in this project on iNaturalist photos (`ml/train.py`) | Code MIT; pretrained weights [torchvision (BSD-3)](https://github.com/pytorch/vision/blob/main/LICENSE) | Species probabilities plus a "not a mushroom" class. Runs **on the phone, offline**, as ONNX. |
| 2. Vision-language model | **[Gemma 4 26B A4B](https://huggingface.co/google/gemma-4-26B-A4B-it)** (Google DeepMind, open weights; 26B-parameter MoE with ~4B active per step), via the [Gemini API](https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api), model id `gemma-4-26b-a4b-it` | [Apache 2.0 — Gemma 4 license](https://ai.google.dev/gemma/docs/gemma_4_license) | Extracts distinguishing features from the photo as **structured JSON** (volva at the stem base, ring, gill colour, underside type, substrate); powers a Turkish assistant grounded in the species knowledge base. |
| 3. Safety rules | — | MIT | **Worst-candidate rule**: if any candidate is deadly/poisonous with ≥5% probability, the result is RED. Gemma's findings can **only raise** the risk, never lower it. |

### Example: how Gemma 4 raises the risk
The image model sees a mushroom as 70% "meadow mushroom". Gemma 4 detects a **volva at the stem base** → the rule layer moves the result to **RED**: *"A volva is visible at the stem base. This is the most important sign of the deadly death cap group."*

```
Photo ─┬─► [1] EfficientNet-B0 (on device) ──► top-5 species + is it a mushroom?
       │                                          │
       └─► [2] Gemma 4 (server → Gemini API) ───► visual features (JSON)
                                                  │
                    [3] Safety rules ◄────────────┘
                    • worst-candidate rule        → 🔴 Possibly poisonous
                    • uncertainty threshold (60%) → 🟡 Not sure
                    • Gemma risk escalation       → ⚪ Low-risk candidate (expert check required)
                                                  → ⛔ Not a mushroom
                    ▼
    Result + look-alike warnings + symptom onset + first aid + Kastamonu calendar
```

## Results (test set — 1,779 photos the model never saw in training)

| Metric | Value |
|---|---:|
| Correct species first (top-1) / in top 5 (top-5) | **90.7% / 98.6%** |
| Deadly species photo shown **RED** | **99.3%** |
| Deadly or poisonous species photo shown **RED** | **98.5%** |
| **Dangerous confusion** (poisonous → "low-risk candidate") | **0.8%** |
| Poisonous species classified as "not a mushroom" | 0% |
| Calibration error (ECE), with temperature scaling | 0.110 → 0.018 |
| Inference time on the phone (ONNX, offline) | ~0.14 s |

The model struggles with some species on its own (e.g. *Armillaria mellea*, recall 70.8%). Thanks to the **worst-candidate rule**, 99.3% of deadly-species photos are still shown RED: the AI and the safety rules work together. Details: [`results/egitim_raporu.md`](results/egitim_raporu.md).

### External test: photos found on the internet
iNaturalist photos look alike (in hand, close-up). To measure real-world use, the model was also tested on **315 Wikimedia Commons photos** from a different source that it never saw (`ml/commons_test.py`, `ml/eval_dis.py`). The first version was weak on internet and screen photos. We added **robustness augmentation** to training (rotation, zoom-out, colour temperature, blur, noise) and **multi-view inference** to the app (centre crop + full image + mirror, averaged probabilities):

| Commons (315 photos) | First model | Final model + multi-view |
|---|---:|---:|
| top-1 | 75.6% | **78.4%** |
| top-5 | 91.4% | **94.6%** |
| Dangerous species → RED | 93.8% | **94.6%** |

On the iNaturalist test set the same model reaches **91.2%** top-1 with multi-view. Details: [`results/dis_test.json`](results/dis_test.json).

### We also measured Gemma 4's contribution
151 test photos were run two ways: image model only, and image model + Gemma 4 (`ml/eval_gemma.py`). Details: [`results/gemma_degerlendirme.md`](results/gemma_degerlendirme.md).

| | Model only | Model + Gemma 4 |
|---|---:|---:|
| Poisonous/deadly species → RED (n=80) | 98.8% | 98.8% |
| Unnecessary RED alarm on low-risk species (n=48) | — | **0%** |
| Gemma API errors (151 photos) | — | **0** |

On this test set the image model already showed 98.8% of dangerous species as RED, so Gemma's risk escalation did not rescue any additional photo. It also caused no false alarms. Gemma spotted the volva at the stem base in only 8% of *Amanita* photos (n=24): iNaturalist photos are single-angle and the stem base is usually hidden in the soil. That is why the app asks separately for a "stem base" photo. Today Gemma's main contributions are **explainability** (showing which sign it saw on the anatomy photo) and the **Mybear assistant**. On photos where the image model struggles, it acts as a second safety net.

## Features
- 📷 **Scan:** three photo slots (cap top, cap underside, stem base). The image model and Gemma 4 run **in parallel**. The result shows the risk, the top 5 species and "dangerous look-alikes". Gemma's findings light up on anatomy markers over a real death cap photo (the volva marker turns red when found).
- 🐻 **Mybear (Gemma 4):** a chat bubble in the corner. Answers stream in, and with no internet it answers from the guide in **offline mode**. Example questions: "List the mushrooms in Kastamonu", "I ate a mushroom I don't trust, what should I do?", "How do I tell a death cap from Caesar's mushroom?". Under the hood:
  - full catalogue of the 27 species, plus details of the species relevant to the question (RAG);
  - formatted bullet-point answers;
  - forbidden phrases filtered out.
- 📖 **Guide:** 27 species, including the local **saçak** (coral fungi) and **koçak** (hen-of-the-woods). Each has a CC-licensed photo with attribution and covers:
  - toxicity, symptoms, onset time, first aid;
  - size, growth cycle, a Kastamonu note;
  - Türkiye observation records (GBIF), iNaturalist/GBIF and clinical literature sources.
- 📅 **Calendar:** a month picker (species count per month, deadly-species warning) plus that month's species, and a full-year phenology table.
- 🚨 **I ate it!:** 114 (National Poison Information Centre) and 112, plus a symptom timeline: symptoms starting later than 6 hours trigger a deadly poisoning warning.
- 📱 **Mobile:** PWA you can add to the home screen, works offline including fonts; ready for an Android/iOS package via Capacitor.

**Speed:** Gemma 4's "thinking" step is limited with `thinkingLevel: minimal`. Two-photo visual analysis dropped from **~180 s → ~5 s** while finding the same features in our measurements (configurable with `MYCOGUARD_THINKING`).

## Quick start

```bash
git clone https://github.com/SelamiKalay/BAKLAVA.git
cd BAKLAVA
```

**1. Get a Gemini API key** (Gemma 4 is on the free tier): https://aistudio.google.com/apikey

**2. Start the app** (Python 3.10+ only, no extra packages):

```bash
GEMINI_API_KEY=<your-key> python server/app.py
```

Open `http://localhost:8000` in your browser. Without a key, or offline, the app keeps working with the image model and the safety rules; the Gemma step shows as "unavailable".

**Another provider** (any OpenAI-compatible endpoint, e.g. DigitalOcean Serverless Inference, Hugging Face, vLLM, Ollama):

```bash
MYCOGUARD_LLM=openai OPENAI_BASE_URL=https://.../v1 OPENAI_API_KEY=... MYCOGUARD_MODEL=<model-id> python server/app.py
```

**Running on a phone and deploying the server:** [`docs/mobil.md`](docs/mobil.md) — DigitalOcean App Platform (`.do/app.yaml`) and Capacitor (Android/iOS).

> **Privacy:** in the Gemma 4 step, photos and questions are sent through the server to the Google Gemini API; on the free tier Google may use this data to improve its products. Species prediction, the guide, the calendar and the emergency screen run entirely on the phone and send no data.

## Data and model pipeline (to reproduce)

```bash
pip install -r requirements-ml.txt
python ml/collect.py        # 1. raw data: iNaturalist photos + GBIF Türkiye records
python ml/clean.py          # 2. cleaning and splitting -> data/clean/ + temizlik_raporu.md
python ml/train.py          # 3. EfficientNet-B0 training -> app/model/*.onnx + results/
python ml/eval_gemma.py     # 4. Gemma 4's contribution (test photos, needs GEMINI_API_KEY in .env)
python ml/thumbs.py         # guide photos (CC-licensed, attributed)
python ml/kaynaklar.py      # iNaturalist/GBIF links for species pages
python src/build_app_data.py
```

**Training speed:** on its first run `ml/train.py` decodes the photos once into a 256×256 cache under `%LOCALAPPDATA%\mycoguard\` (~2.2 GB, outside OneDrive, configurable with `MYCOGUARD_CACHE`). During training it keeps the cache in pinned memory, and augmentation runs batched on the GPU. With classic Windows DataLoader workers we measured ~9.5 s per step while the GPU itself ran at 0.26 s/step; this approach removes that bottleneck. Training needs no internet.

**Data cleaning steps** (`ml/clean.py`, details in `data/clean/temizlik_raporu.md`):
- duplicate records;
- license filter (CC only);
- taxonomy normalisation (subspecies/variety → species);
- broken, tiny or odd-aspect-ratio images;
- **exact and near-duplicate photos via perceptual hashing (dHash)**;
- date and location parsing;
- class balancing;
- **leak-free train/val/test split by observation id**.

On the GBIF side:
- ABSENT records;
- reduction to species level;
- coordinates outside Türkiye, at 0-0 or swapped;
- same species–place–day duplicates;
- province-name normalisation ("KASTAMONU", "Kastamonu İli", "Kastamonu Province" → `kastamonu`).

**Model results:** `results/egitim_raporu.md` covers top-1/top-5 accuracy, per-class recall, calibration (ECE) and the safety metrics. The safety metrics are the poisonous species → RED rate and the **dangerous confusion rate** (a poisonous mushroom shown as "low risk"; target ≈ 0).

## Tests

```bash
python -m pytest -q
```

| Test file | What it checks |
|---|---|
| `tests/test_decide.py` | 8 sample cases, threshold edges, worst-candidate rule, every dangerous species is RED when ranked first |
| `tests/test_species_table.py` | Species table schema, months, symptom hours, look-alikes, dangerous species marked "do not pick", ban on the word "safe" |
| `tests/test_parity.py` | The in-browser `app/decide.js` and `src/decide.py` give the same decision on 2,000 random cases; Gemma escalation (`escalate`) is identical in both languages |
| `tests/test_gemma.py` | Gemma escalation rules, risk never lowered, forbidden-phrase filter, RAG context, Gemini and OpenAI-compatible request formats, off-schema output falls back to safe defaults, rate limit |
| `tests/test_clean.py` | Province/species/date/location parsing, license filter, dHash duplicate detection, leak-free split, balancing |
| `tests/test_train.py` | Training data pipeline (CPU only): centre crop, cache reuse, GPU augmentation, batching |

## Project structure

```
├── app/                  # Mobile-friendly web app (PWA)
│   ├── index.html        #   interface
│   ├── decide.js         #   safety rules (equivalent to Python)
│   ├── model.js          #   on-device ONNX inference (onnxruntime-web)
│   ├── model/            #   trained model + labels
│   └── vendor/ort/       #   onnxruntime-web 1.20.1 (MIT)
├── server/               # Gemma 4 endpoints + static server (no dependencies)
├── ml/                   # collect -> clean -> train -> thumbs
├── src/                  # decision layer (Python) + app data generation
├── data/                 # species_info.csv, demo_cases.json, clean/ (raw/ is not in the repo)
├── results/              # training report, metrics, charts
├── tests/                # pytest
└── docs/                 # data sources, safety & ethics, dev log
```

## Dependencies and licenses

| Component | License |
|---|---|
| KastaMario code | MIT (`LICENSE`) |
| Gemma 4 26B A4B (Gemini API) | [Apache 2.0](https://ai.google.dev/gemma/docs/gemma_4_license) |
| PyTorch / torchvision (EfficientNet-B0 weights) | BSD-3 |
| onnxruntime-web 1.20.1 | MIT |
| IBM Plex Sans, Newsreader (local copy, `app/fonts/`) | SIL Open Font License 1.1 |
| Anatomy photo (`app/img/anatomi.jpg`) | [iNaturalist observation 315054013](https://www.inaturalist.org/observations/315054013), CC0 |
| iNaturalist photos | Each photo's own CC license; attributions in `data/clean/thumbs.json` and `data/clean/inat_clean.csv` |
| GBIF records | CC0 / CC BY / CC BY-NC per record — see `docs/veri-kaynaklari.md` |

## Team

- [@SelamiKalay](https://github.com/SelamiKalay)
- [@emoylmz01](https://github.com/emoylmz01)
- [@rifo5](https://github.com/rifo5)

## Disclaimer
KastaMario is for information only; it does not replace medical advice or expert species identification. The model can make mistakes, which is why the safety rules always assume the worst case. If you ate a wild mushroom, do not wait for symptoms: call **112** or **114** (Türkiye National Poison Information Centre).
