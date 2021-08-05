import aioredis
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app import db_engine
from app import settings

from app.settings import ALGORITHM, SECRET_KEY
from app.authentication import oauth2_scheme
from jose import jwt, JWTError


async def get_db_session() -> AsyncSession:
    # Todo check if having session maker here is okay
    db_session_maker = sessionmaker(
        db_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True
    )
    async with db_session_maker() as session:
        yield session


# Todo see if this is the right way?
async def get_redis() -> aioredis.Redis:
    async with aioredis.from_url(settings.REDIS_URL, decode_responses=True) as redis:
        yield redis
    await redis.close()


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
