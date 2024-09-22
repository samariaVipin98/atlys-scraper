from database.configure import SessionLocal, get_db
from database.models import User
from schema.auth.auth_request import LoginRequest, SignupRequest, Token
from fastapi import APIRouter, Depends, HTTPException, status
from schema.base import base_response as BaseResponse

router = APIRouter(tags=["Authentication"])

@router.post("/signup")
def signup_method(signup_data: SignupRequest, db: SessionLocal = Depends(get_db)):
    try:
        new_user = User.signup(signup_data, db)
        return BaseResponse.BaseResponseWrapper(
        success=True,
        data={"message": "User Created Successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
            headers={"WWW-Authenticate": "Bearer"},
        )
    

@router.post("/login")
def login_method(login_data: LoginRequest, db: SessionLocal = Depends(get_db)):
    try:
        token = User.login(login_data, db)
        return BaseResponse.BaseResponseWrapper(
            success=True,
            data={"message": "User LoggedIn Successfully", "access_token": token})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )