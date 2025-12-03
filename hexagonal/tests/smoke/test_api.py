import requests

BASE_URL = "http://localhost:8081"

def test_create_and_get_order():
    # POST /orders
    resp = requests.post(f"{BASE_URL}/orders", json={"sku": "ABC", "qty": 2})
    assert resp.status_code in (200, 201)
    order_id = resp.json()["id"]

    # GET /orders/:id
    resp2 = requests.get(f"{BASE_URL}/orders/{order_id}")
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["sku"] == "ABC"
    assert data["qty"] == 2
