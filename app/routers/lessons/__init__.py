from fastapi import APIRouter
from app.routers.lessons.radicals import api as radicals_api
from app.routers.lessons.words import api as words_api

api = APIRouter(tags=["Lesson"], prefix="/lessons")

api.include_router(radicals_api)
api.include_router(words_api)
