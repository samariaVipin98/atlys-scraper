from database.configure import Base, engine
from sqlalchemy import Column, Integer, String, Float

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String)

# Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    price = Column(Float)
    image_url = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)