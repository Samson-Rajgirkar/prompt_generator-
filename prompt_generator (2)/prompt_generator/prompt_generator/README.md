# ⚡ PromptForge — AI-Based Dynamic Automated Prompt Generator

A production-ready full-stack Django web application that uses machine learning
to classify user input and dynamically generate optimised AI prompts.

---

## 🖼️ Features

- **ML Text Classification** — TF-IDF + Logistic Regression pipeline (scikit-learn)
  trained on 120+ examples across 6 intent categories
- **Tone Detection** — Rule-based NLP detects 8 tones (formal, casual, technical…)
- **Dynamic Prompt Generation** — Personalised prompt templates assembled from
  classification + tone signals
- **SQLite persistence** — Every input and generated prompt is stored
- **Feedback system** — 1–5 star rating with optional comment, stored in DB
- **History page** — Paginated view of past prompts with collapsible details
- **JSON API** — `POST /api/classify/` for headless / programmatic use
- **Modern UI** — Dark industrial aesthetic, animated probability bars, copy-to-clipboard

---

## 🗂️ Project Structure

```
prompt_generator/
├── manage.py
├── requirements.txt
├── setup.sh                    ← one-command setup
├── README.md
│
├── prompt_generator/           ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── generator/                  ← Main Django app
│   ├── models.py               ← UserInput · GeneratedPrompt · Feedback
│   ├── views.py                ← index · history · submit_feedback · api_classify
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   │
│   ├── ml/                     ← Machine Learning module
│   │   ├── dataset.py          ← 120+ labelled training samples
│   │   ├── train.py            ← TF-IDF + LogReg pipeline training & saving
│   │   ├── predictor.py        ← classify() — inference + prompt generation
│   │   └── saved_models/       ← pipeline.pkl (auto-created on first run)
│   │
│   ├── templates/generator/
│   │   ├── base.html
│   │   ├── index.html          ← Form + result + feedback
│   │   └── history.html
│   │
│   └── static/generator/
│       ├── css/style.css       ← Full design system
│       └── js/main.js          ← Interactions (counter, copy, stars, AJAX)
│
└── ml_training/
    └── train_model.py          ← Standalone retraining script
```

---

## 🚀 Quick Start

### Option A — Automated (recommended)

```bash
git clone <repo-url>
cd prompt_generator
bash setup.sh
```

Then open **http://127.0.0.1:8000**

---

### Option B — Manual step-by-step

**1. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Train the ML model**

```bash
python ml_training/train_model.py
```

Expected output:
```
==================================================
  Model Training Complete
  Accuracy : 95.83%
==================================================
              precision    recall  f1-score
  analytical       1.00      0.80      0.89
  ...
```

**4. Apply database migrations**

```bash
python manage.py makemigrations generator
python manage.py migrate
```

**5. (Optional) Create a superuser for Django Admin**

```bash
python manage.py createsuperuser
```

**6. Run the development server**

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🔌 JSON API

`POST /api/classify/`

**Request body:**
```json
{ "text": "Help me write a pitch deck for my startup" }
```

**Response:**
```json
{
  "category": "business",
  "confidence": "94.2%",
  "tone": "persuasive",
  "generated_prompt": "You are a seasoned business strategist...",
  "all_probabilities": {
    "business": 0.9421,
    "creative": 0.0210,
    ...
  }
}
```

---

## 🧠 Machine Learning Details

| Component      | Choice                              |
|----------------|-------------------------------------|
| Vectoriser     | TF-IDF (unigrams + bigrams, 10k features) |
| Classifier     | Logistic Regression (C=5, lbfgs)   |
| Categories     | creative · technical · analytical · educational · business · conversational |
| Tones          | formal · casual · detailed · concise · creative · technical · persuasive · simple |
| Training set   | 120 labelled examples (20 per category) |
| Framework      | scikit-learn Pipeline               |

### Re-training with custom data

Add samples to `generator/ml/dataset.py` in the `TRAINING_DATA` list, then:

```bash
python ml_training/train_model.py
```

---

## 🗄️ Database Models

```
UserInput
├── input_text     TextField
├── category       CharField (6 choices)
└── timestamp      DateTimeField

GeneratedPrompt
├── input_reference  FK → UserInput (OneToOne)
├── prompt_text      TextField
├── tone             CharField (8 choices)
├── confidence_score FloatField (0–1)
└── timestamp        DateTimeField

Feedback
├── generated_prompt  FK → GeneratedPrompt (OneToOne)
├── rating            IntegerField (1–5)
├── comment           TextField (optional)
└── timestamp         DateTimeField
```

---

## 🛠️ Development

**Run tests:**
```bash
python manage.py test generator
```

**Retrain model:**
```bash
python ml_training/train_model.py
```

**Access admin panel:**
```
http://127.0.0.1:8000/admin/
```

---

## 📦 Dependencies

| Package       | Version  | Purpose                  |
|---------------|----------|--------------------------|
| Django        | ≥4.2     | Web framework            |
| scikit-learn  | ≥1.3.0   | ML pipeline              |
| numpy         | ≥1.24.0  | Numerical operations     |

---

## 📄 License

MIT – Free for personal and commercial use.
