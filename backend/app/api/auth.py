from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    name: str
    email: str
    password_hash: str

@router.post("/register")
def register_user(name: UserRegister):
    return {"message": f"User {name.username} created via APIRouter!"}
