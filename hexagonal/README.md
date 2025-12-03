 Hexagonal Architecture — Orders Service

Цей проєкт реалізує сервіс замовлень у стилі Hexagonal Architecture (Ports & Adapters).  
Ядро не знає про інфраструктуру, а адаптери взаємозамінні (Postgres або CSV).



Ціль

- core/ містить лише домен, порти та юзкейси.
- adapters/ реалізують порти (HTTP, DB, File).
- config/ відповідає за DI та вибір адаптера через ENV.
- Перемикання між Postgres та CSV робиться лише через зміну ENV.

Структура

hexagonal/ ├── core/ │ ├── domain/ # Order entity │ ├── ports/ # OrderRepository interface │ └── usecases/ # CreateOrder, GetOrder │ ├── adapters/ │ ├── http/ # FastAPI controllers │ ├── db/ # PostgresOrderRepository │ └── file/ # CsvOrderRepository │ ├── config/ │ └── factory.py # DI фабрика, вибір адаптера через ENV │ ├── tests/ │ ├── core/ # Юніт-тести ядра │ └── smoke/ # Smoke-тести API (POST/GET) │ ├── Dockerfile ├── docker-compose.yml ├── .env.example └── README.md



ENV

`.env.example`:
PORT=8081 REPO_ADAPTER=db # або file DB_NAME=orders DB_USER=postgres DB_PASS=postgres DB_HOST=db CSV_PATH=/data/orders.csv

Код

---

Запуск

 Підготовка
```bash
cp .env.example .env
2. Запуск через Docker Compose
bash
docker compose up --build
Якщо REPO_ADAPTER=db → використовується Postgres.

Якщо REPO_ADAPTER=file → використовується CSV‑файл (/data/orders.csv).