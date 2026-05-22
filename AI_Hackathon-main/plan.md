# План разработки проекта "Bozor-Analitika"

## Структура проекта
- `frontend/`: Веб-интерфейс (HTML/CSS).
- `parser/`: Скрипты для сбора рыночных данных.
- `ai-services/`: (В разработке) Сервисы для обработки и анализа данных.

## AI Интеграция: Основные направления

1. **Сбор и парсинг данных (Data Ingestion)**
   - **Задача:** Извлечение информации из jett.uz, использовать будем Puppeteer server implementation либо browseract либо playwright.
   - **AI решение:** LLM (GPT-4o/Claude) для извлечения сущностей, OCR для изображений.

2. **Очистка и нормализация (Data Normalization)**
   - **Задача:** Категоризация и сведение товаров к единому виду.
   - **AI решение:** Semantic Matching (Embeddings + Vector DB).

3. **Аналитика и прогнозирование (Predictive Analytics)**
   - **Задача:** Определение рыночной стоимости и прогнозирование спроса.
   - **AI решение:** Time Series Analysis, Anomaly Detection.

4. **Рекомендательная система (Matching Engine)**
   - **Задача:** Предложение лучших B2B-сделок.
   - **AI решение:** Hybrid Matching (Бизнес-правила + Learning to Rank).

## Roadmap

1. **Phase 1 (Setup):** Интеграция AI-сервисов (FastAPI) с существующим `frontend/` и `parser/`.
2. **Phase 2 (Data):** Настройка ETL-пайплайна (сбор -> нормализация -> Vector DB).
3. **Phase 3 (Intelligence):** Разработка прогнозных моделей и рекомендательного движка.


## Idea
Siz taklif qilgan loyiha g‘oyasining qisqacha mazmuni (Summary):
Loyiha nomi: Bozor-Analitika (B2B AI Platform)
Muammo:
O‘zbekiston bozorlarida real vaqtdagi narx-navo, talab va taklifni kuzatish imkonini beruvchi yagona va markazlashgan tahliliy ma’lumotlar bazasining mavjud emasligi. Bu holat ulgurji va chakana savdogarlar uchun eng maqbul narxlarni topishni qiyinlashtiradi.
Yechim va G‘oya:
Real vaqt rejimida an’anaviy bozorlardagi narxlarni tahlil qiluvchi va eng arzon, qulay takliflarni topishga yordam beruvchi aqlli savdo-axborot tizimi.
Kengaytirilgan funksiyalar (Sizning qo‘shimchangiz):
Fond bozori integratsiyasi: Platformaga aksiyalar va xomashyo birjasi narxlari ham kiritiladi. Foydalanuvchilarga nafaqat real bozorda, balki fond bozorida ham aksiyalarni sotib olish yoki sotish imkoniyati yaratiladi.
Sun’iy intellekt (AI Assistant): Tizimga o‘rnatilgan AI yordamchisi ulgurji bozor narxlari bilan aksiyadorlik kompaniyalari ko‘rsatkichlari o‘rtasidagi bog‘liqlikni tahlil qiladi va foydalanuvchilarga bashoratlar hamda savdo bo‘yicha aqlli tavsiyalar beradi.
Eslatma (Moliyaviy ogohlantirish): Fond bozori va aksiyalar savdosi yuqori moliyaviy xavf (risk) bilan bog‘liq. Platformani ishlab chiqishda foydalanuvchilarni ushbu xavflardan ogohlantiruvchi tizim va qonuniy litsenziyalash talablariga rioya qilish muhim hisoblanadi.