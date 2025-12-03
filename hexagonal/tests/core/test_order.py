import pytest
from core.domain.order import Order

def test_qty_validation():
    with pytest.raises(ValueError):
        Order("ABC", 0)
