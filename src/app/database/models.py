from datetime import timedelta
import os
from fastapi import HTTPException, Depends, Request, status
from database.configure import SessionLocal
from repo.users.user_repo import check_password, create_access_token, get_password_hash, verify_access_token
from database.configure import Base, engine
from sqlalchemy import Column, Float, Integer, String

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String)

    @classmethod
    def create(cls, username: str, password: str, email: str, db):
        password_hash = get_password_hash(password)
        new_user = cls(username=username, password_hash=password_hash, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @classmethod
    def get(cls, username: str, db):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def signup(cls, signup_data, db):
        db_user = cls.get(signup_data.username, db)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        else:
            new_user = cls.create(db, signup_data.username, signup_data.password, signup_data.email)
            return new_user

    @classmethod
    def login(cls, login_data, db):
        db_user = cls.get(login_data.username, db)
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        
        password_hash_bytes = db_user.password_hash.encode('utf-8')
        
        if check_password(login_data.password.encode('utf-8'), password_hash_bytes):
            access_token_expires = timedelta(minutes=int(os.getenv("TOKEN_EXPIRY_IN_MINS", 30)))
            access_token = create_access_token(username=db_user.username, expires_delta=access_token_expires)
            return access_token
        else:
            raise HTTPException(status_code=400, detail="Invalid password")

    @classmethod
    def get_current_user(cls, request: Request, db):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # Extract token from the Authorization header
        if "authorization" not in request.headers:
            raise credentials_exception
        
        token = request.headers['authorization'].split(" ")[1]
        token_data = verify_access_token(token, credentials_exception)
        db_user = cls.get(token_data.username, db)
        if db_user is None:
            raise credentials_exception
        return db_user

        
# Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    price = Column(Float)
    image_url = Column(String)

    

# Create the database tables
Base.metadata.create_all(bind=engine)