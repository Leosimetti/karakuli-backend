from fastapi import APIRouter, Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import CookieAuthentication
from .db import db
import os


SECRET = os.getenv("SECRET", "VERY133331235VERYsdad211SECRETPHRASENOONEKNOWS")


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, db["users"])


async def on_after_register(user: UserDB, request: Request):
    from .db import db
    review_db = db["reviews"]
    user_db = review_db[str(user.id)]
    await user_db.create_index("word_id", unique=True)
    await user_db.create_index([("review_date",1)])
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)
cookie_authentication = CookieAuthentication(
    secret=SECRET, lifetime_seconds=3600, cookie_name="karakuli-cookie"
)

router = APIRouter()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication, cookie_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_auth_router(cookie_authentication), prefix="/auth/cookie", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
