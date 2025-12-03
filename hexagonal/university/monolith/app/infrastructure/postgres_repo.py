import psycopg2
from app.domain.product import Product
class PostgresProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def create(self, product: Product) -> Product:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products(name, price) VALUES (%s, %s) RETURNING id",
                (product.name, product.price)
            )
            product.id = cur.fetchone()[0]
            self.conn.commit()
        return product

    def list(self) -> list[Product]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM products")
            rows = cur.fetchall()
        return [Product(id=r[0], name=r[1], price=float(r[2])) for r in rows]
