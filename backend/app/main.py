from fastapi import FastAPI
from app.database.connection import test_connection


app = FastAPI()
test_connection()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}