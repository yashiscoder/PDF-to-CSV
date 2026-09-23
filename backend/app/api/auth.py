from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


@router.post("/register")
def register_user(user: UserRegister):
    return {
        "message": f"User {user.name} created via APIRouter!"
    }