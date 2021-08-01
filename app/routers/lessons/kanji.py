from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_db_session
from app.models import Word, Kanji
from app.scrapper import kanji

api = APIRouter(tags=["Kanji"], prefix="/kanji")


@api.post(
    "/parse",
    status_code=status.HTTP_200_OK,
)
async def parse(
        session: AsyncSession = Depends(get_db_session),
):
    if await Word.get_by_id(session, 3) is not None:  # Todo remove this retarded if
        return "Already parsed"
    else:
        gen = kanji()
        for _ in range(50):
            w = next(gen)
            word = await Kanji.create(session, dict=w)
            session.add(word)
            await session.commit()

    return "Done"