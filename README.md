# Arbitra AI — O'zbekiston Fond Bozori Analitika Platformasi

O'zbekiston fond bozori aksiyalari, kompaniyalari va sun'iy intellekt yordamchisini o'z ichiga olgan veb-platforma.

## Texnologik stack

| Komponent | Texnologiya |
|-----------|-------------|
| **Backend** | Django 5.x, Python, Whitenoise |
| **AI mikroservis** | FastAPI + google-generativeai |
| **Frontend** | HTML, Tailwind CSS (CDN), Chart.js, Lightweight Charts |
| **Ma'lumotlar bazasi** | SQLite (Django ORM) |
| **AI model** | Google Gemini 1.5 Flash (httpx) |
| **Parser** | BeautifulSoup, requests, pytest |
| **Auth** | Django built-in (session-based) |

## Loyiha tuzilishi

```
├── manage.py
├── requirements.txt
├── config/                        # Django settings
│   ├── settings.py                # SQLite, uz locale, Asia/Tashkent, WhiteNoise
│   ├── urls.py                    # URL routing (admin, api, static files)
│   ├── wsgi.py
│   └── asgi.py
├── backend/                       # Django app
│   ├── models.py                  # 6 model: Company, Stock, StockHistory, Plan, FAQ, ChatHistory
│   ├── views.py                   # 9 view: market_data, stocks, companies, plans, faq, chat, auth
│   ├── urls.py                    # 13 API endpoint
│   ├── admin.py                   # Admin panel
│   ├── services/
│   │   └── gemini.py              # Google Gemini API integratsiyasi (httpx)
│   ├── management/commands/
│   │   └── load_data.py           # JSON dan DB ga ma'lumot import qilish
│   └── migrations/
├── frontend/                      # Static HTML fayllar
│   ├── landing_paage.html         # Landing page
│   ├── index.html                 # Bosh sahifa (auth talab qiladi)
│   ├── AiAssistent.html           # AI chat sahifasi
│   ├── aksiyalar.html             # Aksiyalar ro'yxati
│   ├── bozor.html                 # Bozor ma'lumotlari
│   ├── sharx.html                 # Stock detail chart
│   ├── demo_chart.html            # Demo chartlar
│   ├── profil.html                # Foydalanuvchi profili
│   ├── css/main.css               # Dark/light mode CSS
│   ├── logo_fixed.jpg
│   ├── logo_night.jpg
│   └── parser/                    # Ma'lumot yig'uvchi (standalone)
│       ├── main.py                # Sintetik data generator + jett.uz scraper
│       ├── test_parser.py         # Pytest testlari
│       ├── requirements.txt
│       └── data/bozor_data.json   # Generatsiya qilingan bozor ma'lumotlari
└── ai-services/                   # AI mikroservis (FastAPI)
    └── main.py                    # POST /api/chat endpoint (google-generativeai SDK)
```

## API endpointlar

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/market/` | To'liq bozor ma'lumoti (stocks, companies, plans, faq) |
| GET | `/api/stocks/` | Aksiyalar ro'yxati |
| GET | `/api/companies/` | Kompaniyalar ro'yxati |
| GET | `/api/plans/` | Tarif rejalari |
| GET | `/api/faq/` | FAQ |
| POST | `/api/chat/` | AI chat (`message` + `context` JSON) |
| POST | `/api/auth/login/` | Login (`username` + `password` JSON) |
| GET | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Joriy foydalanuvchi ma'lumoti |
| GET | `/admin/` | Django admin panel |

## O'rnatish va ishga tushirish

```bash
# 1. Virtual environment yaratish
python -m venv .venv
source .venv/bin/activate

# 2. Dependensiyalarni o'rnatish
pip install -r requirements.txt

# 3. .env faylini yaratish
# .env ga GEMINI_API_KEY va DJANGO_SECRET_KEY ni kiriting

# 4. Ma'lumotlar bazasini yaratish
python manage.py migrate
python manage.py load_data

# 5. Superuser yaratish
python manage.py createsuperuser

# 6. Serverni ishga tushirish
python manage.py runserver 0.0.0.0:5000
```

Server `http://localhost:5000` da ishlaydi.

### AI mikroservis (ixtiyoriy)

```bash
cd ai-services
pip install fastapi uvicorn google-generativeai python-dotenv
uvicorn main:app --reload --port 5001
```

### Parser testlari

```bash
cd frontend/parser
pip install -r requirements.txt
pytest test_parser.py -v
```

## Muhit o'zgaruvchilari (.env)

| O'zgaruvchi | Tavsif |
|---|---|
| `DJANGO_SECRET_KEY` | Django maxfiy kaliti |
| `GEMINI_API_KEY` | Google Gemini API kaliti (AI chat uchun) |
| `DEBUG` | True/False (default: True) |

## Ma'lumotlar manbai

1. **Sintetik data** — `frontend/parser/main.py` orqali deterministik generatsiya (51 ta aksiya, 260 kunlik tarix)
2. **jett.uz scraping** — real tarif rejalari va FAQ ma'lumotlari
3. Ma'lumotlar `bozor_data.json` da saqlanadi va `python manage.py load_data` orqali DB ga import qilinadi

## Litsenziya

MIT
