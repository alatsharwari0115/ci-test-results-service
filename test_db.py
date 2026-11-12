import pytest
import db

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db,'DB_PATH',str(tmp_path / "test.db"))
    db.init_db()

def test_inserted_results_appear_in_list():
    db.insert_result("test_login", "failed", "abc123", 120)
    assert db.list_results() == [{"test_name": "test_login", "status": "failed", "commit_sha": "abc123", "duration_ms": 120}]

def test_data_survieves_after_reinitialization():
    db.insert_result("test_login", "failed", "abc123", 120)
    db.init_db()
    assert len(db.list_results()) ==1

def test_flaky_test_is_flagged():
    db.insert_result("test_login", "failed", "abc123", 120)
    db.insert_result("test_login", "passed", "abc123", 120)
    assert db.find_flaky_tests() == [{'test_name': 'test_login', 'commit_sha': 'abc123'}]

def test_consistent_failures_not_flagged_as_flaky():
    db.insert_result("test_login", "failed", "abc123", 120)
    db.insert_result("test_login", "failed", "abc123", 120)
    assert db.find_flaky_tests() == []

def test_different_results_on_different_commits_not_flagged():
    db.insert_result("test_login", "failed", "abc123", 120)
    db.insert_result("test_login", "passed", "xyz123", 120)
    assert db.find_flaky_tests() == []







