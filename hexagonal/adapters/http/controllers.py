from fastapi import FastAPI, HTTPException
from core.usecases.create_order import CreateOrder
from core.usecases.get_order import GetOrder

def create_app(repo):
    app = FastAPI()

    @app.post("/orders")
    def create_order(data: dict):
        sku, qty = data["sku"], data["qty"]
        order_id = CreateOrder(repo).execute(sku, qty)
        return {"id": order_id}

    @app.get("/orders/{order_id}")
    def get_order(order_id: str):
        order = GetOrder(repo).execute(order_id)
        if not order:
            raise HTTPException(status_code=404)
        return {"id": order.id, "sku": order.sku, "qty": order.qty}

    return app
