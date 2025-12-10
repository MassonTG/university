from fastapi import FastAPI

app = FastAPI(title="Catalog Service")

ITEMS = [
    {"id": 1, "name": "Desk"},
    {"id": 2, "name": "Chair"},
]

@app.get("/items")
def list_items():
    return ITEMS
