from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_returns_running_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"CI test results service is running"}

def test_returns_404_given_non_existent_service():
    response = client.get("/nope")
    assert response.status_code == 404

def test_post_valid_result_returns_201():
    response = client.post("/results", json={
        "test_name": "test_login",
        "status": "passed",
        "commit_sha": "abc123",
        "duration_ms": 120,
    })
    assert response.status_code == 201
    

def test_post_invalid_status_returns_422():
    response = client.post("/results", json={
        "test_name": "test_login",
        "status": "maybe",
        "commit_sha": "abc123",
        "duration_ms": 120,
    })
    assert response.status_code == 422
    error = response.json()['detail']
    assert error[0]['loc'] == ['body','status']

def test_post_missing_commit_sha_returns_422():
    response = client.post("/results", json = {
        "test_name": "test_login",
        "status": "failed",
        "duration_ms": 120,})
    assert response.status_code == 422
    error = response.json()['detail']
    assert error[0]['loc'] == ['body','commit_sha']
    
