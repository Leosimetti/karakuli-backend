from fastapi import APIRouter

from app.routers.lists.common import api as common_api
from app.routers.lists.items import api as items_api

api = APIRouter(tags=["Study List"], prefix="/lists")

api.include_router(common_api)
api.include_router(items_api)
