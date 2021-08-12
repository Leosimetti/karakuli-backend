from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.depends import get_db_session
from app.models import Lesson
from app.routers.lessons.radicals import api as radicals_api
from app.routers.lessons.words import api as words_api
from app.routers.lessons.kanji import api as kanji_api

api = APIRouter(tags=["Lesson"], prefix="/lessons")


@api.get(
    "/{lesson_id}",
    status_code=status.HTTP_200_OK,
)
async def get(
        lesson_id: int,
        session: AsyncSession = Depends(get_db_session),
):
    lesson = await Lesson.get_by_id(session, lesson_id)

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Lesson not found.'
        )

    lesson = await Lesson.get_content(session, lesson_id)
    return lesson

api.include_router(radicals_api)
api.include_router(words_api)
api.include_router(kanji_api)
