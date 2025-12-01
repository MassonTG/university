# Monolith — FastAPI + Postgres + Redis

Этот проект — учебный **Layered Monolith** на базе FastAPI, Postgres и Redis.  
Он демонстрирует архитектуру с разделением на слои (Domain, Application, Infrastructure, Presentation), контейнеризацию через Docker и автоматизацию через Makefile.

---

Запуск проекта

1. Клонирование репозитория
git clone https://github.com/MassonTG/university.git
cd university/monolith
2. Настройка окружения
Скопируйте пример переменных окружения:
cp .env.example .env
Отредактируйте .env, указав свои значения (например, пароль к Postgres).
3. Запуск через Docker Compose
bash
docker compose up --build
После запуска:
API будет доступен на http://localhost:8080
Health-check: http://localhost:8080/health
Redis используется для кеширования списка продуктов
4. Проверка API
bash
 Добавить продукт
Invoke-RestMethod http://localhost:8080/products `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name":"Desk","price":199.9}'
 Получить список продуктов
Invoke-RestMethod http://localhost:8080/products


Тестирование
Запуск тестов:
bash
make test
Тесты лежат в папке tests/ и покрывают:
Domain (модель продукта)
Application (use cases)
Smoke-тесты API

Структура проекта
Код
monolith/
├── app/
│   ├── domain/          # Бизнес-логика (модели, сущности)
│   ├── application/     # Use cases (сценарии работы)
│   ├── infrastructure/  # Хранилища, миграции, Postgres/Redis
│   └── presentation/    # Контроллеры FastAPI
├── tests/               # Юнит- и интеграционные тесты
├── Dockerfile           # Сборка приложения
├── docker-compose.yml   # Поднятие Postgres, Redis, API
├── requirements.txt     # Python-зависимости
├── environment.example  # Пример переменных окружения
├── Makefile             # Удобные команды (up, down, test, redis-cli)
└── README.md            # Документация

Зачем нужны __init__.py
Я добавил __init__.py во все папки (domain, application, infrastructure, presentation, tests), чтобы:
Python воспринимал их как пакеты, а не просто папки
Работали импортируемые модули (from app.domain.product import Product)
Упрощалась навигация и поддержка структуры проекта
Тесты могли корректно находить код и запускаться без ошибок импорта
Без этих файлов Python не видел бы внутренние директории как пакеты, и ловил ошибки ModuleNotFoundError.

Makefile команды
make up — поднять проект через Docker Compose
make down — остановить контейнеры
make test — запустить тесты
make redis-cli — открыть Redis CLI
