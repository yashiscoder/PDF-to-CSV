from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User
from app.core.security import hash_password, verify_password


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

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": f"User {user.name} created successfully!"
    }

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    no_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not no_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email has not Registered"
        )

    if not verify_password(user.password, no_email.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    return {
        "message": "Login successful!"
    }