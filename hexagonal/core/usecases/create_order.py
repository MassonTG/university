from core.domain.order import Order

class CreateOrder:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, sku: str, qty: int) -> str:
        order = Order(sku, qty)
        return self.repo.create(order)
