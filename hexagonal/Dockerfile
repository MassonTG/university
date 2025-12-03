# Використовуємо офіційний Python образ
FROM python:3.11-slim

# Робоча директорія
WORKDIR /app

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY . .

# ENV для порту
ENV PORT=8081

# Запускаємо FastAPI через Uvicorn
CMD ["python", "main.py"]
