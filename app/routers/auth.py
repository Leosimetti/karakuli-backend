from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserGeneralResponse, UserCreate
from app.models import User as UserTable

from app.settings import logger
from app import get_db_session

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
    user_db = UserTable(**user.dict())
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
