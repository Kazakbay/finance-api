from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Finance API working"}


def test_add_transaction():
    response = client.post("/add?amount=1000&category=food")
    assert response.status_code == 200
    assert response.json()["amount"] == 1000
    assert response.json()["category"] == "food"


def test_list_transactions():
    response = client.get("/list")
    assert response.status_code == 200
    assert "transactions" in response.json()
