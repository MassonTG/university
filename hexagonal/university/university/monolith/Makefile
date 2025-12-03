# Makefile для Layered Monolith

# Запуск системи
up:
    docker compose up --build -d

# Зупинка системи
down:
    docker compose down

# Перегляд логів API
logs:
    docker compose logs -f api

# Запуск юніт-тестів у контейнері
test:
    docker compose run --rm api pytest

# Виконання SQL-міграцій вручну
migrate:
    docker compose exec db psql -U $$DB_USER -d $$DB_NAME -f /docker-entrypoint-initdb.d/migrations.sql

# Відкрити Redis CLI для перевірки кешу
redis-cli:
    docker compose exec redis redis-cli
