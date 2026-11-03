from fastapi import HTTPException
from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel

app = FastAPI()

class ResultIn(BaseModel):
    test_name: str
    status: Literal["passed","failed"]
    commit_sha: str
    duration_ms: int

results: list[ResultIn] = []

@app.get("/")
def read_root():
    return {"message": "CI test results service is running"}

@app.get("/health")
def heath():
    return {"status": "ok"}

@app.get("/boom")
def boom():
    raise Exception ("something broken")

@app.get("/unavailable")
def unavailable():
    raise HTTPException(status_code=503, detail="database not reachable")

@app.post("/results",status_code=201)
def add_result(result:ResultIn):
    results.append(result)
    return {"stored": len(results)}

@app.get("/results")
def get_results():
    return results