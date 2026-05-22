# Инструкция по запуску проекта

Этот проект состоит из бэкенда (Python/Flask), фронтенда (HTML/JS) и сервисов ИИ (Python/FastAPI).

## Предварительные требования
- Установленный Python 3.x
- Установленный Node.js (для управления зависимостями фронтенда)
- Настроенный файл `.env` в корневой директории с ключом `GEMINI_API_KEY`:
  ```
  GEMINI_API_KEY=your_actual_api_key_here
  ```

---

## 1. Настройка Бэкенда
Для работы основного сервера:
1. Перейдите в папку `backend`:
   ```bash
   cd backend
   ```
2. Установите зависимости (рекомендуется использовать виртуальное окружение):
   ```bash
   python -m venv venv
   # Активация:
   # Windows: .\venv\Scripts\activate
   # Linux/macOS: source venv/bin/activate
   pip install flask httpx
   ```
3. Запуск сервера:
   ```bash
   python server.py
   ```
   Сервер будет доступен по адресу `http://localhost:5000`.

---

## 2. Настройка ИИ-сервисов
Для работы вспомогательных ИИ-сервисов:
1. Перейдите в папку `ai-services`:
   ```bash
   cd ai-services
   ```
2. Используйте имеющееся виртуальное окружение или создайте новое:
   ```bash
   # Windows:
   .\venv\Scripts\activate
   pip install fastapi uvicorn google-generativeai python-dotenv
   ```
3. Запуск сервиса:
   ```bash
   uvicorn main:app --reload
   ```

---

## 3. Настройка Фронтенда
Фронтенд является статическим, но использует библиотеку `lightweight-charts`.
1. Перейдите в папку `frontend`:
   ```bash
   cd frontend
   ```
2. Установите зависимости (если необходимо):
   ```bash
   npm install
   ```
Фронтенд обслуживается напрямую через основной бэкенд-сервер на Flask. После запуска `backend/server.py`, откройте браузер и перейдите на `http://localhost:5000`.
