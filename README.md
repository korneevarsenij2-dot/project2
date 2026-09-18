🏎️ AMG Cyber Luxury Store API
Высокопроизводительный асинхронный REST API сервис для управления каталогом премиальной техники, авторизацией пользователей, моментальным кэшированием профилей и интеграцией с курсами валют Центробанка РФ.
🛠️ Стек технологий (Tech Stack)
Язык: Python 3.11+
Фреймворк: FastAPI (Async)
База данных: PostgreSQL + SQLAlchemy 2.0 (AsyncSession, selectinload)
Кэширование & NoSQL: Redis (TTL кэширование + инвалидация при сделках)
Безопасность: JWT (JSON Web Tokens) + Bcrypt хэширование паролей
Внешние интеграции: HTTPX (асинхронный клиент к API ЦБ РФ с обработкой таймаутов)
Тестирование: Pytest + FastAPI TestClient (интеграционные тесты эндпоинтов)
Валидация: Pydantic v2 (Strict Schema Validation)
🏛️ Архитектура проекта
Проект построен по модульному принципу с разделением обязанностей (Clean Decoupled Architecture):
project2/
├── routers/              # Эндпоинты по бизнес-доменам
│   ├── auth.py          # Регистрация, авторизация, профиль /me с кэшем
│   └── luxury.py        # Сделки покупки, конвертер валют
├── services/             # Слой внешних интеграций
│   └── external_api.py  # HTTPX клиент к API Центробанка
├── tests/                # Автоматические тесты
│   └── test_api.py      # Интеграционные тесты на Pytest
├── .env                  # Секретные ключи (в gitignore)
├── .gitignore            # Защита секретов и байткода
├── database.py           # Асинхронные пулы PostgreSQL и клиент Redis
├── models.py             # ORM модели таблиц БД
├── schemas.py            # Pydantic схемы валидации
├── security.py           # Логика хэширования и JWT-аутентификации
├── requirements.txt      # Зафиксированные версии зависимостей
└── mainn.py              # Точка входа и регистрация роутеров
⚡️ Ключевые архитектурные решения
Redis Caching & Invalidation (Cache-Aside Pattern):
Запрос GET /auth/me кэшируется в оперативной памяти Redis на 60 секунд. Время ответа — менее 2 мс.
При совершении транзакции (POST /luxury/buy_supercar / POST /luxury/buy_bike) происходит немедленная инвалидация устаревшего кэша (redis_client.delete), исключая рассинхронизацию баланса.
Внешняя интеграция без зависаний (HTTPX):
Запрос к API Центробанка выполняется через асинхронный контекстный менеджер с жестким таймаутом (timeout=10.0).
Реализована обработка сетевых сбоев (TimeoutException, HTTPError) с отдачей корректных статус-кодов (502, 504).
Безопасность данных:
Пароли никогда не хранятся в открытом виде, хэшируются через односторонний алгоритм Bcrypt.
Схемы ответов UserResponseSchema исключают поле hashed_password из JSON-выдачи клиенту.
🚀 Инструкция по локальному запуску
1. Клонирование репозитория
git clone https://github.com/ваш-логин/amg-backend.git
cd amg-backend
2. Создание и активация виртуального окружения
python -m venv .venv
# Для Windows:
.venv\Scripts\activate
# Для Linux/macOS:
source .venv/bin/activate
3. Установка всех зависимостей
pip install -r requirements.txt
4. Настройка переменных окружения
Создайте файл .env в корне проекта:
SECRET_KEY=your_super_secret_jwt_key
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/mydb
REDIS_URL=redis://localhost:6379/0
5. Запуск сервера разработки
uvicorn mainn:app --reload
Документация Swagger UI доступна по адресу: http://127.0.0.1:8000/docs
🧪 Запуск автоматических тестов
pytest -v
Тесты проверяют работоспособность конвертера валют и защищённость закрытых эндпоинтов без авторизации.