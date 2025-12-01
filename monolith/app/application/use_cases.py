from app.domain.product import Product

class ProductRepository:
    def create(self, product: Product) -> Product: ...
    def list(self) -> list[Product]: ...

class CreateProduct:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def execute(self, dto: dict) -> Product:
        product = Product(id=None, name=dto["name"], price=dto["price"])
        product.validate()
        return self.repo.create(product)

class ListProducts:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def execute(self) -> list[Product]:
        return self.repo.list()
