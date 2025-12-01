from fastapi import FastAPI, HTTPException
from app.application.use_cases import CreateProduct, ListProducts
from app.infrastructure.postgres_repo import PostgresProductRepository
import psycopg2, os, redis, json

app = FastAPI()

# Postgres
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)
repo = PostgresProductRepository(conn)

# Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products")
def get_products():
    cache_key = "products"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    products = [p.__dict__ for p in ListProducts(repo).execute()]
    redis_client.setex(cache_key, 30, json.dumps(products))  # TTL=30s
    return products

@app.post("/products", status_code=201)
def create_product(dto: dict):
    try:
        product = CreateProduct(repo).execute(dto)
        redis_client.delete("products")  # invalidate cache
        return product.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
