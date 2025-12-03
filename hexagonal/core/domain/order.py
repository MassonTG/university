import uuid

class Order:
    def __init__(self, sku: str, qty: int):
        if qty <= 0:
            raise ValueError("Quantity must be > 0")
        self.id = str(uuid.uuid4())
        self.sku = sku
        self.qty = qty
