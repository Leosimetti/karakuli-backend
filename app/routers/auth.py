from fastapi import APIRouter, status, Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app import get_db_session
from app.authentication import hash, create_access_token, verify, get_current_user
from app.settings import logger

from app.schemas.auth import Token
from app.models import User as UserTable
from app.schemas.user import UserGeneralResponse, UserCreate

# logger = getLogger(__name__)

api = APIRouter(tags=["auth"], prefix="/auth")


@api.post(
    "/register",
    response_model=UserGeneralResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_a_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_db_session),
):
    """
    Creates a unverified user in the database
    and sends the verification email.
    """
    user_db = UserTable(**user.dict(exclude={"password"}), password=hash(user.password))
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    logger.info(f"User {user} registered")

    return user_db


@api.post(
    "/request-verify",
    response_model=str,
    status_code=status.HTTP_200_OK,
)
def request_verification_token():
    # if user is already verified - say NO-NO
    # if Not logged in            - do nothing
    # if ok                       - return token
    return "DEFECATION_REQUESTED"


@api.post(
    "/verify",
    response_model=UserGeneralResponse,
    status_code=status.HTTP_200_OK,
)
def verify_user(token: str):
    return "VERIFIED"


@api.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    user = await UserTable.get_by_email(db, request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@api.post(
    '/refresh-token',
    response_model=Token,
    responses={
        401: {'description': 'Email or password incorrect'},
    }
)
async def refresh_token(user: UserTable = Depends(get_current_user())):
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
