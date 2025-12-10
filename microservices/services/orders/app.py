from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Orders Service")

class CreateOrder(BaseModel):
    userId: int
    itemId: int
    qty: int

ORDERS = []
ORDER_SEQ = 1

@app.post("/orders", status_code=201)
def create_order(payload: CreateOrder):
    global ORDER_SEQ
    if payload.qty <= 0:
        raise HTTPException(status_code=400, detail="qty must be > 0")
    order = {"id": ORDER_SEQ, "userId": payload.userId, "itemId": payload.itemId, "qty": payload.qty}
    ORDERS.append(order)
    ORDER_SEQ += 1
    return {"id": order["id"]}
