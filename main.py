from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "CI test results serivice is running"}

@app.get("/health")
def heath():
    return {"status": "ok"}