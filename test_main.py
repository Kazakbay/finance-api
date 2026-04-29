from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base
from dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def register_and_login(email='test@client.com', password='testpass'):
    client.post("/register", json={"email": email, "password": password})
    response = client.post(
        "/login",
        data = {"username": email, "password": password}
    )
    return response.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --- Tests ---

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Finance API working"}


def test_register():
    response = client.post(
        "/register",
        json = {"email": "test@test.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"
    assert "hashed_password" not in response.json()


def test_register_duplicate_email():
    client.post("/register", json = {"email": "test@test.com", "password": "testpass"})
    response = client.post(
        "/register",
        json = {"email": "test@test.com", "password": "testpass"}
    )
    assert response.status_code == 400


def test_login():
    client.post("/register", json={"email": "test@test.com", "password": "testpass"})
    response = client.post(
        "/login",
        data = {"username": "test@test.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_add_transaction():
    token = register_and_login()
    print(f"\nТОКЕН: {token}")
    response = client.post(
        "/add",
        json = {"amount": 1000, "category": "food"},
        headers=auth_headers(token)
    )
    print(f"\nОТВЕТ: {response.json()}")
    assert response.status_code == 200
    assert response.json()["amount"] == 1000
    assert response.json()["category"] == "food"


def test_add_transaction_unauthorized():
    response = client.post("/add", json={"amount":1000, "category": "food"})
    assert response.status_code == 401


def test_list_transactions():
    token = register_and_login()
    client.post("/add", json={"amount": 1000, "category": "food"}, headers=auth_headers(token))
    client.post("/add", json={"amount": 500, "category": "transport"}, headers=auth_headers(token))

    response = client.get("/list", headers=auth_headers(token))
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_only_own_transactions():
    token1 = register_and_login("user1@test.com", "pass1")
    token2 = register_and_login("user2@test.com", "pass2")

    client.post("/add", json={"amount": 1000, "category": "food"}, headers=auth_headers(token1))

    response = client.get("/list", headers=auth_headers(token2))
    assert len(response.json()) == 0


def test_delete_transaction():
    token = register_and_login()
    add = client.post("/add", json={"amount":1000, "category": "food"}, headers=auth_headers(token))
    transaction_id = add.json()["id"]

    response = client.delete(f"/delete/{transaction_id}", headers=auth_headers(token))
    assert response.status_code == 200


def test_delete_someone_else_transaction():
    token1 = register_and_login("user1@test.com", "pass1")
    token2 = register_and_login("user2@test.com", "pass2")

    add = client.post("/add", json={"amount": 1000, "category": "food"}, headers=auth_headers(token1))
    transaction_id = add.json()["id"]

    response = client.delete(f"/delete/{transaction_id}", headers=auth_headers(token2))
    assert response.status_code == 404