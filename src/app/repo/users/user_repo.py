import os
from database.configure import SessionLocal, get_db
from database.models import User
from schema.auth.auth_request import LoginRequest, SignupRequest, TokenData
from fastapi import HTTPException, Depends, Header, Request, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    hashed_pwd = pwd_context.hash(password)
    return hashed_pwd

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"username": username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
    return encoded_jwt

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(request: Request, db: SessionLocal = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Extract token from the Authorization header
    if not request.headers["authorization"]:
        raise credentials_exception
    
    token = token = request.headers['authorization'].split(" ")[1]
    token_data = verify_access_token(token, credentials_exception)
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def generate_token(db, login_data: LoginRequest):
    db_user = get_user_by_username(db, login_data.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(login_data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=int(os.getenv("TOKEN_EXPIRY_IN_MINS")))
    access_token = create_access_token(username=db_user.username, expires_delta=access_token_expires)
    return access_token

def create_user(db, signup_data: SignupRequest):
    db_user = get_user_by_username(db, signup_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        hashed_password = get_password_hash(signup_data.password)
        new_user = User(username=signup_data.username, password_hash=hashed_password, email=signup_data.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True