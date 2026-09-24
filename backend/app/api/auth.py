from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User


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
    duplicate_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )
    if duplicate_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )
    return {
        "message": f"User {user.name} created via APIRouter!"
    }