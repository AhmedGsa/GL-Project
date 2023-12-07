from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
from typing import Annotated
from fastapi.security import HTTPBearer
import os

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_HOURS = os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()

class JWT():
    def create_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=int(ACCESS_TOKEN_EXPIRE_HOURS))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return token

    def verify_token(token: Annotated[str, Depends(bearer_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token.credentials, SECRET_KEY, ALGORITHM)
        except JWTError:
            raise credentials_exception
        return payload