import psycopg2
from core.domain.order import Order
from core.ports.order_repository import OrderRepository

class PostgresOrderRepository(OrderRepository):
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def create(self, order: Order) -> str:
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO orders (id, sku, qty) VALUES (%s, %s, %s)",
                            (order.id, order.sku, order.qty))
        return order.id

    def get_by_id(self, order_id: str) -> Order | None:
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, sku, qty FROM orders WHERE id=%s", (order_id,))
                row = cur.fetchone()
                if row:
                    o = Order(row[1], row[2])
                    o.id = row[0]
                    return o
        return None
