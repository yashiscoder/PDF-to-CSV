# app/api/test.py
from fastapi import APIRouter

router = APIRouter()


# Change @router@get to @router.get
@router.get("/test")
def test_endpoint():
    return {"message": "Test router is working"}