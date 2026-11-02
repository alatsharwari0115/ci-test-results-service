from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_heath_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_availability():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"CI test results serivice is running"}