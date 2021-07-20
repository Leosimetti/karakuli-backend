from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta

from app.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from sqlalchemy.ext.asyncio import AsyncSession

from app import get_db_session
from app.schemas.auth import Token, TokenData
from app.models.user import User

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(*fields_to_load) -> callable:
    async def _get_current_user(
            token: str = Depends(oauth2_scheme),
            session: AsyncSession = Depends(get_db_session)
    ) -> User:

        try:
            user_id = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])['user_id']

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Bad token.',
                headers={'WWW-Authenticate': 'Bearer'}
            )

        user = await User.get_by_id(session, user_id, *fields_to_load)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found.',
                headers={'WWW-Authenticate': 'Bearer'}
            )

        return user

    return _get_current_user


def hash(pwd: str):
    return pwd_context.hash(pwd)


def verify(hashed_pwd, plain_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)
