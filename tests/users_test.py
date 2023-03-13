from fastapi.testclient import TestClient
from app.orm_main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get("message") == "Hello World"
