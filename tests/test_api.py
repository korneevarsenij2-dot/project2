from fastapi.testclient import TestClient
from mainn import app

client = TestClient(app)

def test_convert_price_usd():
    response = client.get("/luxury/price_usd/1000000")
    assert response.status_code == 200
    data = response.json()
    assert "price_usd" in data
    assert data["price_rub"] == 1000000
def test_me_without_token_forbidden():
    response = client.get("/auth/me")
    assert response.status_code == 401
