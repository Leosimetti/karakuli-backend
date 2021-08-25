from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication import hash
from app.depends import get_current_user, get_db_session
from app.models import User as UserTable
from app.schemas.user import UserCreate, UserGeneralResponse
from app.settings import logger

api = APIRouter(tags=["Common auth"])


@api.post(
    "/register",
    response_model=UserGeneralResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_a_user(
    user: UserCreate = Depends(UserCreate.as_form),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Creates a unverified user in the database
    and sends the verification email.
    """
    # Todo @todo send EMAIL
    # Todo @todo add checks for credentials (if already exists)

    tmp = await UserTable.get_by_email(session, user.email)
    if tmp:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User already exists"
        )

    user_db = UserTable(**user.dict(exclude={"password"}), password=hash(user.password))
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    logger.info(f"User {user} registered")

    return user_db


# Todo @todo add proper return model to hide some fields
@api.get("/me")
async def get_current_user(user=Depends(get_current_user())):
    return user


@api.post(
    "/request-verify",
    response_model=str,
    status_code=status.HTTP_200_OK,
)
def request_verification_token():
    # Todo @todo implement
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
    # Todo @todo implement
    return "VERIFIED"
