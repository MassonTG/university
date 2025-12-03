class FakeRepo:
    def __init__(self): self.store = {}
    def create(self, order): self.store[order.id] = order; return order.id
    def get_by_id(self, id): return self.store.get(id)

def test_create_and_get_order():
    from core.usecases.create_order import CreateOrder
    from core.usecases.get_order import GetOrder
    repo = FakeRepo()
    order_id = CreateOrder(repo).execute("ABC", 2)
    order = GetOrder(repo).execute(order_id)
    assert order.sku == "ABC"
    assert order.qty == 2
