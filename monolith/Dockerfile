# Builder stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY app/ app/
USER nobody
CMD ["uvicorn", "app.presentation.controllers:app", "--host", "0.0.0.0", "--port", "8080"]

HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1
