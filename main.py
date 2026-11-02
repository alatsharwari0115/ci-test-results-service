from fastapi import HTTPException
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "CI test results serivice is running"}

@app.get("/health")
def heath():
    return {"status": "ok"}

@app.get("/boom")
def boom():
    raise Exception ("something broken")

@app.get("/unavailable")
def unavailable():
    raise HTTPException(status_code=503, detail="database not reachable")