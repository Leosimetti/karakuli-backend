from fastapi import HTTPException, APIRouter
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication import create_access_token, verify
from app.depends import get_db_session, get_current_user
from app.models import User as UserTable
from app.schemas.auth import Token

api = APIRouter(tags=["JWT"], prefix="/jwt")


@api.post('/login')
async def jwt_login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    user = await UserTable.get_by_email(db, request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


# Todo check if this is implemented the right way, as it seems kind of pointless
# When your token expires, this function cannot refresh it. It only works when the token is still valid
# Todo mb make it so that the token can still be refreshed a minute after the actual expiration? But hoW?
@api.post(
    '/refresh',
    response_model=Token,
    responses={
        401: {'description': 'Email or password incorrect'},
    }
)
async def refresh_jwt_token(user: UserTable = Depends(get_current_user())):
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
