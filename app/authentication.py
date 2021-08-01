from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

from app.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

from app import app as app_object

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=app_object.router.prefix + "/auth/jwt/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash(pwd: str):
    return pwd_context.hash(pwd)


def verify(hashed_pwd, plain_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
