# CI Test Results Service

A backend service that collects CI test results and flags flaky tests.

## Features
- Collects test results from CI pipelines through a REST API, with request validation
- Stores results in SQLite, so data survives restarts
- Detects flaky tests: a test is flaky when it both passed and failed on the **same commit**

## API
| Method | Path | Description |
|---|---|---|
| GET | `/` | Service message |
| GET | `/health` | Health check |
| POST | `/results` | Store a test result. Returns `201` and the new `id`, or `422` for invalid input |
| GET | `/results` | List all stored results |
| GET | `/flaky` | List tests with mixed results on the same commit |

Example request body for `POST /results`:
```json
{
  "test_name": "test_login",
  "status": "passed",
  "commit_sha": "abc123",
  "duration_ms": 120
}
```
`status` must be `passed` or `failed`.

## How Flakiness Is Defined
Results are grouped by test name and commit. If a group contains both `passed` and `failed`, the test is flagged for that commit. This separates flaky tests from consistently broken tests and from regressions across commits.

## Tech Stack
- **Language:** Python
- **Framework:** FastAPI (validation with Pydantic)
- **Database:** SQLite
- **Testing:** pytest

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Interactive API docs are at `http://127.0.0.1:8000/docs`.

## Run Tests
```bash
pytest -v
```
Tests use a temporary database, so they never touch real data.

## Roadmap
- Flakiness rate per test across commits
- Docker image
- GitHub Actions CI pipeline
- Move from SQLite to PostgreSQL

## Status
In progress
