from fastapi import APIRouter

api = APIRouter(tags=["Study List"], prefix="/lists")

from app.routers.lists import common
from app.routers.lists import items
