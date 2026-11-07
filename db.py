import sqlite3
from main import results

DB_PATH = "results.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                status TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                duration_ms INTEGER NOT NULL
            )
        """)

def insert_results(test_name, status, commit_sha, duration_ms):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO results (test_name, status, commit_sha, duration_ms) VALUES (?, ?, ?, ?)",
            (test_name, status, commit_sha, duration_ms),
        )
    return cur.lastrowid

def list_results():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT test_name, status, commit_sha, duration_ms FROM results ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]