from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_db_session
from app.models import Word, Kanji
from app.scrapper import kanji

api = APIRouter(tags=["Kanji"], prefix="/kanji")

# TODO PLZ DO NOT FORGET TO REMOVE THIS IN PROD OR YOU ARE RETARD
import os

if os.getenv("IS_DEV"):
    @api.post(
        "/parse",
        status_code=status.HTTP_200_OK,
    )
    async def parse(
            session: AsyncSession = Depends(get_db_session),
    ):
        if await Kanji.get_by_kanji(session, "亜"):  # Todo remove this retarded if
            return "Already parsed"
        else:
            gen = kanji()
            for _ in range(50):
                w = next(gen)
                await Kanji.create(session, dict=w)

        return "Done"
