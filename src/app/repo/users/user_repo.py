from database.configure import SessionLocal, get_db
from repo.utils.utils import verify_access_token
from database.models import User
from fastapi import Depends, HTTPException, Request, status


def get_current_user(request: Request, db: SessionLocal = Depends(get_db)):
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
    db_user = User.get(token_data.username, db)
    if db_user is None:
        raise credentials_exception
    return db_user