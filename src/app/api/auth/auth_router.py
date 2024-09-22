from database.configure import SessionLocal, get_db
from database.models import User
from repo.users.user_repo import create_user, generate_token
from schema.auth.auth_request import LoginRequest, SignupRequest, Token
from fastapi import APIRouter, Depends

router = APIRouter(tags=["Authentication"])

@router.post("/signup")
def signup(user: SignupRequest, db: SessionLocal = Depends(get_db)):
    user = create_user(db, user)
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: SessionLocal = Depends(get_db)):
    token = generate_token(db, login_data)
    return {"access_token": token}