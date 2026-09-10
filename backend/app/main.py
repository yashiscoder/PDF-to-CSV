from fastapi import FastAPI
from app.api.test import router as test_router

app = FastAPI()
app.include_router(test_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}