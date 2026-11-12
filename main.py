from fastapi import HTTPException
from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel
from contextlib import asynccontextmanager
import db

@asynccontextmanager
async def lifespan(app):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)

class ResultIn(BaseModel):
    test_name: str
    status: Literal["passed","failed"]
    commit_sha: str
    duration_ms: int

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
    new_id = db.insert_result(result.test_name,result.status,result.commit_sha,result.duration_ms)
    return {'id':new_id}
   
@app.get("/results")
def get_results():
    return db.list_results()

@app.get("/flaky")
def flaky_tests():
    return db.find_flaky_tests()
