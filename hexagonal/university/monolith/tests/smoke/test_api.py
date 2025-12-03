import requests

BASE = "http://localhost:8080"

def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code