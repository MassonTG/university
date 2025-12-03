import csv, os
from core.domain.order import Order
from core.ports.order_repository import OrderRepository

class CsvOrderRepository(OrderRepository):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id","sku","qty"])

    def create(self, order: Order) -> str:
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([order.id, order.sku, order.qty])
        return order.id

    def get_by_id(self, order_id: str) -> Order | None:
        with open(self.path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == order_id:
                    o = Order(row["sku"], int(row["qty"]))
                    o.id = row["id"]
                    return o
        return None
