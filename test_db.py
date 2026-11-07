import db

def test_inserted_results_appear_in_list(tmp_path,monkeypatch):
    monkeypatch.setattr(db,"DB_PATH", str(tmp_path / "test.db"))
    db.init_db()

    db.insert_results("test_login", "failed", "abc123", 120)

    assert db.list_results() == [{"test_name": "test_login", "status": "failed", "commit_sha": "abc123", "duration_ms": 120}]


