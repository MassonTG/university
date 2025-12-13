
Event-Driven Demo (Kafka)

Ціль
Побудова мінімального event-driven стеку з Kafka, який демонструє асинхронну взаємодію сервісів через події.

Структура проєкту

event-driven/
  docker-compose.yml
  README.md
  schemas/
    order_created.json
    payment_captured.json
    email_sent.json
  services/
    orders/
      Dockerfile
      package.json
      server.js
    billing/
      Dockerfile
      package.json
      server.js
    notifications/
      Dockerfile
      package.json
      server.js


## Події та топік
- Топік: `orders.events`
- OrderCreated `{ orderId, userId, itemId, qty, ts }`
- PaymentCaptured `{ orderId, amount, ts }`
- EmailSent `{ orderId, to, ts }`

JSON‑схеми для кожної події знаходяться в папці `schemas/`.

## Сервіси
- orders → приймає HTTP POST `/orders`, генерує `OrderCreated`
- billing → слухає `OrderCreated`, ідемпотентно генерує `PaymentCaptured`
- notifications → слухає `PaymentCaptured`, лог/імітація відправки email, генерує `EmailSent`

## Запуск
1. Перейти в корінь проєкту:
   ```powershell
   cd C:\Users\andrew\Desktop\event-driven
   ```

2. Запустити стек:
   ```powershell
   docker-compose up --build
   ```
   Це підніме Zookeeper, Kafka, створить топік `orders.events`, і запустить три сервіси.

3. Створити замовлення:
   ```powershell
   irm http://localhost:5002/orders -Method Post -Body '{"userId":1,"itemId":2,"qty":1}' -ContentType "application/json"
   ```
   → у відповідь повернеться JSON замовлення.

## Перевірка логів
Подивитися список контейнерів:
```powershell
docker ps
```

Перевірити логи:
```powershell
docker logs event-driven-billing-1
docker logs event-driven-notifications-1
```

Очікувано:
- У `billing`:
  ```
  Billing processed { orderId: 1, amount: 100, ts: ... }
  ```
- У `notifications`:
  ```
  Sending email { orderId: 1, to: 'user@test.com', ts: ... }
  ```

## Приймальні критерії
- Повторна публікація `OrderCreated` з тим самим `orderId` не дублює платіж:
  ```
  Billing skipped duplicate OrderCreated for orderId 1
  ```
- Документація формату подій є в `schemas/`.

##  Тести
1. Створити кілька замовлень → перевірити, що кожне проходить повний ланцюжок.
2. Повторити замовлення з тим самим `orderId` → у `billing` має бути повідомлення про пропуск дубліката.
3. Переконатися, що `notifications` завжди генерує `EmailSent`.


