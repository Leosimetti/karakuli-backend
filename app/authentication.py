from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette import status

from app.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES

from app import app as app_object, redis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=app_object.router.prefix + "/auth/jwt/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    await redis.set(data["user_id"], encoded_jwt)

    return encoded_jwt


def hash(pwd: str):
    return pwd_context.hash(pwd)


async def get_user_by_refresh_token(token: str):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='The token has expired.',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad token.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user_id = user["user_id"]
    redis_token = await redis.get(user_id)
    if redis_token == token:
        return user_id


def verify(hashed_pwd, plain_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
