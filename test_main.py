from fastapi.testclient import TestClient
import pytest
from main import app
import db

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db,'DB_PATH',str(tmp_path / "test.db"))
    db.init_db()
    print(tmp_path)

client = TestClient(app)

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_returns_running_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"CI test results service is running"}

def test_unknown_path_returns_404():
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
    
def test_posted_results_appear_in_the_results_list():
    payload = {"test_name": "test_login","status": "passed","commit_sha": "abc123","duration_ms": 120,}
    post_response = client.post("/results", json = payload)
    assert post_response.status_code == 201

    get_response = client.get("/results")
    assert get_response.status_code == 200
    assert get_response.json() == [payload]

def test_post_results_returns_sequential_ids():
    payload = {"test_name": "test_login","status": "passed","commit_sha": "abc123","duration_ms": 120,}
    first = client.post("/results", json = payload)
    second = client.post("/results", json = payload)
    
    assert first.json() == {'id': 1}
    assert second.json() == {'id': 2}

