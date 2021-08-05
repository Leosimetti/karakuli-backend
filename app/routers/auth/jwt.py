from fastapi import HTTPException, APIRouter
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication import create_access_token, verify, create_refresh_token, get_user_by_refresh_token
from app.depends import get_db_session, get_redis
from app.models import User as UserTable
from app.schemas.auth import Token

api = APIRouter(tags=["JWT"], prefix="/jwt")


async def create_tokens(user_id, redis):
    access_token = create_access_token(data={"user_id": user_id})
    refresh_token = await create_refresh_token(data={"user_id": user_id}, redis=redis)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@api.post('/login',
          responses={
              404: {"detail": "Invalid Credentials/ Incorrect password"},
          })
async def jwt_login(
        request: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db_session),
        redis=Depends(get_redis),
):
    user = await UserTable.get_by_email(db, request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")

    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")

    tokens = await create_tokens(user.id, redis)
    return tokens


# Todo check if this is implemented the right way, as it seems kind of pointless
# Todo mb make it so that the token can still be refreshed a minute after the actual expiration? But hoW?
@api.post(
    '/refresh',
    response_model=Token,
    responses={
        401: {'description': 'Bad token. '},
    }
)
async def refresh_jwt_token(
        refresh_token: str,
        redis=Depends(get_redis)
):
    user_id = await get_user_by_refresh_token(refresh_token, redis)
    tokens = await create_tokens(user_id, redis)

    return tokens
