from fastapi import APIRouter

api = APIRouter(tags=["Auth"], prefix="/auth")

import app.routers.auth.common
import app.routers.auth.jwt
import app.routers.auth.cookie
