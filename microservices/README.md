Microservices Demo (FastAPI + NGINX Gateway)
Цей проєкт демонструє базову архітектуру мікросервісів на основі FastAPI з використанням NGINX як API Gateway.  
Система складається з трьох сервісів:
Catalog – повертає список товарів.
Users – повертає дані користувачів.
Orders – створює замовлення.

Усі сервіси запускаються через Docker Compose, мають healthchecks і доступні через єдиний gateway на порту `8080`.

Запуск

Клонувати репозиторій:
   git clone https://github.com/MassonTG/university.git
   cd university/microservices
Запустити сервіси:
  docker compose up --build
Перевірити статус контейнерів:
  docker compose ps
→ усі сервіси мають бути Up (healthy).
