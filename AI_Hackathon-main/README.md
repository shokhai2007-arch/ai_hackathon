# Arbitra AI — O'zbekiston Fond Bozori Analitika Platformasi

O'zbekiston fond bozori aksiyalari, kompaniyalari va sun'iy intellekt yordamchisini o'z ichiga olgan veb-platforma.

**Loyiha manbasi:** [github.com/alijonov77/AI_Hackathon](https://github.com/alijonov77/AI_Hackathon)

---

## Loyiha haqida

Ushbu loyiha AI Hackathon doirasida yaratilgan bo'lib, O'zbekiston fond bozorini tahlil qilish uchun mo'ljallangan. Platforma 51 ta kompaniya, 17 ta sektor bo'yicha real vaqt rejimidagi (sintetik) aksiyalar ma'lumotlari, interaktiv chart'lar, Google Gemini asosidagi AI yordamchi, foydalanuvchi autentifikatsiyasi va ma'lumot parserini o'z ichiga oladi.

**Muammo:** O'zbekiston bozorlarida narxlar, talab va taklifni kuzatish uchun yagona, markazlashgan analitik ma'lumotlar platformasi mavjud emas.

**Yechim:** An'anaviy bozor ma'lumotlarini fond birjasi integratsiyasi va AI tahlili bilan birlashtirgan platforma.

---

## Texnologik stack

| Komponent | Texnologiya |
|-----------|------------|
| **Asosiy backend** | Django 5.x, Python, Whitenoise |
| **Eski backend** | Flask (legacy, `backend/server.py`) |
| **AI mikroservis** | FastAPI + google-generativeai |
| **Frontend** | HTML, Tailwind CSS (CDN), Chart.js, Lightweight Charts |
| **Ma'lumotlar bazasi** | SQLite (Django ORM) |
| **AI model** | Google Gemini 1.5 Flash (httpx) |
| **Parser** | BeautifulSoup, requests, pytest |
| **Auth** | Django built-in (session-based) |

---

## Loyiha tuzilishi

```
AI_Hackathon-main/
│
├── manage.py                      # Django management entry point
├── requirements.txt               # Python dependensiyalar
├── .env                           # Muhit o'zgaruvchilari (API kalitlari)
│
├── config/                        # Django loyiha sozlamalari
│   ├── settings.py                # Django settings (DB, apps, static, auth)
│   ├── urls.py                    # URL routing (admin, api, static files)
│   ├── wsgi.py                    # WSGI (Gunicorn uchun)
│   └── asgi.py                    # ASGI
│
├── backend/                       # Django asosiy app
│   ├── models.py                  # 6 model: Company, Stock, StockHistory, Plan, FAQ, ChatHistory
│   ├── views.py                   # 9 view: market_data, stocks, companies, plans, faq, chat, auth
│   ├── urls.py                    # 13 API endpoint
│   ├── admin.py                   # Admin panel sozlamalari
│   ├── server.py                  # Legacy Flask server
│   ├── services/
│   │   └── gemini.py              # Google Gemini API integratsiyasi (httpx)
│   ├── management/commands/
│   │   └── load_data.py           # JSON dan DB ga ma'lumot import qilish
│   ├── migrations/
│   │   └── 0001_initial.py        # DB migratsiya
│   ├── .env.example               # .env namunasi
│   │
│   └── templates/                 # Frontend HTML (Django static files)
│       ├── index.html             # Bosh sahifa (auth talab qiladi)
│       ├── AiAssistent.html       # AI chat sahifasi (Gemini)
│       ├── aksiyalar.html         # Aksiyalar ro'yxati
│       ├── bozor.html             # Bozor ma'lumotlari
│       ├── sharx.html             # Stock detail chart (Chart.js + Lightweight Charts)
│       ├── demo_chart.html        # Demo chart'lar
│       ├── profil.html            # Foydalanuvchi profili
│       ├── css/main.css           # Tailwind CSS (bo'sh)
│       │
│       └── parser/                # Ma'lumot yig'uvchi (standalone)
│           ├── main.py            # Sintetik data generator + jett.uz scraper
│           ├── test_parser.py     # Pytest testlari (16 test class)
│           ├── requirements.txt   # beautifulsoup4, requests, pytest
│           └── data/
│               └── bozor_data.json # Generatsiya qilingan bozor ma'lumotlari
│
├── ai-services/                   # AI mikroservis (FastAPI)
│   ├── main.py                    # POST /api/chat endpoint (google-generativeai SDK)
│   └── README.md                  # AI service dokumentatsiyasi
│
├── frontend/                      # Muqobil frontend build (Tailwind)
│   ├── package.json               # tailwindcss, postcss, autoprefixer
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── css/input.css              # Tailwind input + dark mode
│
├── plan.md                        # Rivojlanish rejasi (rus/uz)
├── kelajak_rejalar.md             # Batafsil roadmap (~50 ta band)
└── RUNNING.md                     # Ishga tushirish qo'llanmasi (rus)
```

---

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

---

## O'rnatish va ishga tushirish

```bash
# 1. Virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Dependensiyalar
pip install -r requirements.txt

# 3. .env faylini sozlash
cp backend/.env.example .env
# .env ga GEMINI_API_KEY va DJANGO_SECRET_KEY ni kiriting

# 4. Ma'lumotlar bazasi
python manage.py migrate
python manage.py load_data

# 5. Superuser
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

### Testlarni ishga tushirish

```bash
cd backend/templates/parser
pip install -r requirements.txt
pytest test_parser.py -v
```

---

## Ma'lumotlar manbai

1. **Sintetik data** — `parser/main.py` orqali deterministik generatsiya (51 ta aksiya, 260 kunlik tarix)
2. **jett.uz scraping** — real tarif rejalari va FAQ ma'lumotlari
3. Ma'lumotlar `bozor_data.json` da saqlanadi va `python manage.py load_data` orqali DB ga import qilinadi

---

## Xususiyatlar

- 51 ta kompaniya aksiyalari, 17 ta sektor bo'yicha
- Interaktiv chart'lar (Chart.js + Lightweight Charts)
- Google Gemini AI chat assistenti
- Dark mode (qorong'i / yorug' mavzu)
- Qidiruv va filtr (nomi, sektori bo'yicha)
- Foydalanuvchi autentifikatsiyasi
- Django admin panel
- Sintetik ma'lumot generatori
- Web scraper (jett.uz)

---

## Roadmap

- [x] Django migratsiya (Flask → Django)
- [x] Django admin panel
- [x] Auth tizimi
- [x] API endpointlar
- [x] AI chat assistent
- [x] Dark mode
- [x] Parser (synthetic + scraped data)
- [ ] Playwright real-time data collection
- [ ] PostgreSQL migratsiya
- [ ] WebSocket real-time chart
- [ ] LSTM/Transformer narx bashorati
- [ ] Texnik indikatorlar (SMA, EMA, RSI, MACD)
- [ ] Docker konteynerizatsiya
- [ ] CI/CD (GitHub Actions)
- [ ] Telegram bot
- [ ] Mobil responsive / PWA

---

## Eslatma

Platformadagi ma'lumotlar va AI tavsiyalari faqat ma'lumot olish uchun mo'ljallangan bo'lib, investitsiya maslahati hisoblanmaydi.

## Litsenziya

MIT
