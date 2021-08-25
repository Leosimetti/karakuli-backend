from fastapi import APIRouter

from app.routers.auth.common import api as auth_api
from app.routers.auth.cookie import api as cookie_api
from app.routers.auth.jwt import api as jwt_api

api = APIRouter(tags=["Auth"], prefix="/auth")

api.include_router(auth_api)
api.include_router(jwt_api)
api.include_router(cookie_api)
