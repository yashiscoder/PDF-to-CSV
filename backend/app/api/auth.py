from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class UserRegister(BaseModel):
    name: str
    email: str
    password: str


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    return {
        "message": f"User {user.name} created via APIRouter!"
    }