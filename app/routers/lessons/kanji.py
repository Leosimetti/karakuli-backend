import os
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_db_session
from app.models import Kanji
from app.scrapper import kanji

api = APIRouter(tags=["Kanji"], prefix="/kanji")

# Todo @todo PLZ DO NOT FORGET TO REMOVE THIS IN PROD OR YOU ARE RETARD

if os.getenv("IS_DEV"):

    @api.post(
        "/parse",
        status_code=status.HTTP_200_OK,
    )
    async def parse(
        amount: Optional[int] = 50,
        session: AsyncSession = Depends(get_db_session),
    ):
        if await Kanji.get_by_kanji(session, "亜"):  # Todo @todo remove this retarded if
            return "Already parsed"
        else:
            for _, k in zip(range(amount), kanji()):
                await Kanji.create(session, dict=k)
        return "Done"
