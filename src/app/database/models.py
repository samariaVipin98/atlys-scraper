from datetime import timedelta
import os
from repo.utils.utils import check_password, create_access_token, get_password_hash
from fastapi import HTTPException
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

    

        
# Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    price = Column(Float)
    image_url = Column(String)

    @classmethod
    def create(cls, title:str, price: Float, image_url: str, db):
        new_product = Product(title=title, price=price, image_url=image_url)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product


    @classmethod
    def get(cls, title, db):
        return db.query(cls).filter(Product.title == title).first()
    
    @classmethod
    def update_price(cls, title: str, new_price: Float, db):
        product = cls.get(title, db)
        product.price = new_price
        db.commit()
        db.refresh(product)
        return

# Create the database tables
Base.metadata.create_all(bind=engine)