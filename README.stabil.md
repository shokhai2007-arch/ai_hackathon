# Arbitra AI — Stabil versiya (ai_engineer)

O'zbekiston fond bozori analitikasi uchun veb-platforma. AI_Hackathon-main ning `ai_engineer` branch'idagi stabil tarmog'i.

**Loyiha manbasi:** [github.com/alijonov77/AI_Hackathon](https://github.com/alijonov77/AI_Hackathon) — `ai_engineer` branch

---

## AI_Hackathon-main dan farqi

Bu versiya **AI_Hackathon-main** ning `ai_engineer` branch'idan olingan stabil nusxasi bo'lib, asosiy tashkiliy farq — **frontend fayllarining joylashuvi**:

| Jihat | AI_Hackathon-main | stabil (ai_engineer) |
|-------|-------------------|---------------------|
| Frontend joylashuvi | `backend/templates/` da | Alohida `frontend/` katalogida |
| Static root | `STATICFILES_DIRS = [BASE_DIR / 'backend/templates']` | `STATICFILES_DIRS = [BASE_DIR / 'frontend']` |
| Parser joylashuvi | `backend/templates/parser/` | `frontend/parser/` |
| Branch | `main` / `backend` | `ai_engineer` |
| Qo'shimcha fayllar | — | `landing_paage.html`, `staticfiles/`, `db.sqlite3` |
| .gitignore | yo'q | Bor (14 ta qoida) |

---

## Texnologik stack

| Komponent | Texnologiya |
|-----------|------------|
| **Asosiy backend** | Django 5.x, Python, Whitenoise |
| **Eski backend** | Flask (legacy, `backend/server.py`) |
| **AI mikroservis** | FastAPI + google-generativeai |
| **Frontend** | HTML, Tailwind CSS (CDN), Chart.js, Lightweight Charts |
| **Ma'lumotlar bazasi** | SQLite (Django ORM) — `db.sqlite3` tayyor |
| **AI model** | Google Gemini 1.5 Flash (httpx) |
| **Parser** | BeautifulSoup, requests, pytest |
| **Auth** | Django built-in (session-based) |

---

## Loyiha tuzilishi

```
stabil/                              # (ì«óá∩ »á»¬á)
│
├── manage.py                        # Django management
├── requirements.txt                 # django, python-dotenv, httpx, gunicorn, whitenoise
├── .env                             # Muhit o'zgaruvchilari
├── .gitignore                       # Git ignore qoidalari
├── db.sqlite3                       # Ma'lumotlar bazasi (tayyor)
├── staticfiles/                     # Django static collection
│
├── config/                          # Django sozlamalari
│   ├── settings.py                  # SQLite, uz locale, Asia/Tashkent, WhiteNoise
│   ├── urls.py                      # /admin/, /api/, / (static serve)
│   ├── wsgi.py
│   └── asgi.py
│
├── backend/                         # Django app
│   ├── models.py                    # 6 model
│   ├── views.py                     # 9 view
│   ├── urls.py                      # 13 endpoint
│   ├── admin.py                     # Admin panel
│   ├── server.py                    # Legacy Flask server
│   ├── services/
│   │   └── gemini.py                # Gemini API integratsiyasi
│   ├── management/commands/
│   │   └── load_data.py             # JSON → DB import
│   └── migrations/
│       └── 0001_initial.py
│
├── frontend/                        # Frontend statik fayllar (alohida katalog)
│   ├── index.html                   # Bosh sahifa
│   ├── AiAssistent.html             # AI chat
│   ├── aksiyalar.html               # Aksiyalar ro'yxati
│   ├── bozor.html                   # Bozor ma'lumotlari     (MAVJUD EMAS)
│   ├── sharx.html                   # Stock chart
│   ├── profil.html                  # Profil sahifasi
│   ├── demo_chart.html              # Demo chart'lar
│   ├── landing_paage.html           # Landing page (qo'shimcha)
│   ├── css/main.css                 # Dark/light mode CSS
│   ├── package.json                 # lightweight-charts dep
│   ├── node_modules/                # NPM paketlar
│   │
│   └── parser/                      # Ma'lumot yig'uvchi
│       ├── main.py                  # Sintetik data + jett.uz scraper
│       ├── test_parser.py           # Pytest (30+ test)
│       ├── requirements.txt
│       └── data/
│           └── bozor_data.json
│
├── ai-services/                     # AI mikroservis (FastAPI)
│   ├── main.py                      # POST /api/chat
│   └── README.md
│
├── server_stdout.log                # Flask server loglari
├── server_stderr.log
├── plan.md                          # Rivojlanish rejasi
├── kelajak_rejalar.md               # Roadmap
└── RUNNING.md                       # Ishga tushirish (rus)
```

**Eslatma:** AI_Hackathon-main da mavjud bo'lgan `bozor.html` sahifasi ushbu branch'da yo'q.

---

## API endpointlar

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/market/` | To'liq bozor ma'lumoti |
| GET | `/api/stocks/` | Aksiyalar |
| GET | `/api/companies/` | Kompaniyalar |
| GET | `/api/plans/` | Tarif rejalari |
| GET | `/api/faq/` | FAQ |
| POST | `/api/chat/` | AI chat |
| POST | `/api/auth/login/` | Login |
| GET | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Joriy foydalanuvchi |
| GET | `/admin/` | Admin panel |

---

## O'rnatish va ishga tushirish

```bash
# 1. Virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Dependensiyalar
pip install -r requirements.txt

# 3. .env faylini tekshirish (GEMINI_API_KEY mavjudligiga)
cat .env

# 4. DB migratsiya (agar db.sqlite3 bo'lmasa)
python manage.py migrate

# 5. Ma'lumotlarni yuklash
python manage.py load_data frontend/parser/data/borzor_data.json

# 6. Superuser
python manage.py createsuperuser

# 7. Serverni ishga tushirish
python manage.py runserver 0.0.0.0:5000
```

### Legacy Flask versiya

```bash
pip install flask httpx python-dotenv
python backend/server.py
```

### AI mikroservis

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

---

## Muhim farqlar (AI_Hackathon-main vs stabil)

| Xususiyat | AI_Hackathon-main | stabil |
|-----------|------------------|--------|
| Frontend katalogi | `backend/templates/` | `frontend/` |
| Parser | `backend/templates/parser/` | `frontend/parser/` |
| `bozor.html` | bor | yo'q |
| `landing_paage.html` | yo'q | bor |
| .gitignore | yo'q | bor |
| db.sqlite3 | generatsiya qilinadi | tayyor |
| Branch | `main` / `backend` | `ai_engineer` |
| npm dependency | `lightweight-charts` (frontend/) | `lightweight-charts` (frontend/) |

---

## Roadmap

- [x] Django migratsiya (Flask → Django)
- [x] Admin panel
- [x] Auth tizimi
- [x] API endpointlar
- [x] AI chat assistent
- [x] Dark mode
- [x] Parser
- [ ] Playwright real-time data
- [ ] PostgreSQL
- [ ] WebSocket chart
- [ ] ML narx bashorati
- [ ] Docker
- [ ] CI/CD
- [ ] Telegram bot

---

## Eslatma

Platforma ma'lumotlari va AI tavsiyalari investitsiya maslahati emas.

## Litsenziya

MIT
