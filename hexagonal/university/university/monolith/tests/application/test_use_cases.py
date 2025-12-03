import pytest
from application.use_cases import CreateProduct, ListProducts
from domain.product import Product

class MockRepo:
    def __init__(self):
        self.items = []
    def create(self, product: Product) -> Product:
        product.id = 1
        self.items.append(product)
        return product
    def list(self):
        return self.items

def test_create_valid_product():
    repo = MockRepo()
    use_case = CreateProduct(repo)
    product = use_case.execute({"name":"Desk","price":100})
    assert product.id == 1

def test_list_products():
    repo = MockRepo()
    repo.create(Product(id=None, name="Desk", price=100))
    use_case = ListProducts(repo)
    assert len(use_case.execute()) == 1
