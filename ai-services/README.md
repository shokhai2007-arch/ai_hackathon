# Bozor-Analitika AI Xizmatlari

Ushbu modul **FastAPI** asosida qurilgan backendni o‘z ichiga oladi, u **Gemini API** bilan integratsiya qilish uchun vositachi (proxy) bo‘lib xizmat qiladi. U frontenddan kelayotgan so‘rovlarni qabul qiladi, ularni tizimli kontekst bilan boyitadi va foydalanuvchilar uchun aqlli javoblarni oladi.

## Asosiy imkoniyatlar
- **Gemini uchun Proxy:** Google Gemini API'siga so‘rovlarni yo‘naltirish.
- **Kontekst inyeksiyasi:** Foydalanuvchi so‘rovlarini bozor haqidagi kontekst (kompaniyalar, tariflar, FAQ, aksiyalar) bilan to‘ldirish.
- **REST API:** AI-yordamchi bilan muloqot qilish uchun oddiy interfeys.

## O‘rnatish va ishga tushirish

### 1. Muhitni tayyorlash
Python 3.10+ o‘rnatilganligiga ishonch hosil qiling. `ai-services/` papkasida virtual muhit yarating:

```bash
python -m venv venv
# Faollashtirish (Windows)
.\venv\Scripts\activate
```

### 2. Bog‘liqliklarni (dependencies) o‘rnatish
```bash
pip install -r requirements.txt
```

### 3. Muhit o‘zgaruvchilarini sozlash
Loyihaning ildiz papkasida yoki `ai-services/` ichida `.env` faylini yarating va u yerga API kalitingizni qo‘shing:

```text
GEMINI_API_KEY=google_ai_studio_dan_olingan_api_kalitingiz
```

### 4. Serverni ishga tushirish
```bash
uvicorn main:app --reload --port 5000
```
Server `http://127.0.0.1:5000` manzilida ishga tushadi.

## API Endpoint'lar

- **GET `/status`**: Serverning ishlash holatini tekshirish.
- **POST `/api/chat`**: AI bilan muloqot qilish uchun asosiy endpoint.
    - **Body**:
        ```json
        {
          "message": "Agrobankning narxi qanday?",
          "context": "AI uchun kontekst ma'lumotlari..."
        }
        ```

## Texnologik stek
- **FastAPI**: API uchun yuqori unumli freymvork.
- **Google Generative AI SDK**: Gemini bilan ishlash uchun rasmiy kutubxona.
- **Pydantic**: So‘rov ma'lumotlarini validatsiya qilish.
