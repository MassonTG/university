import pytest
from domain.product import Product

def test_invalid_name():
    with pytest.raises(ValueError):
        Product(id=None, name="", price=10).validate()

def test_invalid_price():
    with pytest.raises(ValueError):
        Product(id=None, name="Desk", price=-5).validate()
