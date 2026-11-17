from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_online():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"


def test_negative_item_returns_400():
    response = client.get("/items/-1")
    assert response.status_code == 400
