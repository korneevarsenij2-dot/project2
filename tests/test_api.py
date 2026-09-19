from fastapi.testclient import TestClient
from mainn import app

client = TestClient(app)

def test_convert_price_usd_success():
    response = client.get("/luxury/price_usd/1000000")
    assert response.status_code == 200
    data = response.json()
    assert "price_usd" in data
    assert data["price_rub"] == 1000000


def test_me_without_token_unauthorized():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_invalid_price_format():
    response = client.get("/luxury/price_usd/not_a_number")
    assert response.status_code == 422


def test_buy_nonexistent_car_without_token():
    response = client.post("/luxury/buy_supercar", json={"supercar_id": 99999})
    assert response.status_code == 401
