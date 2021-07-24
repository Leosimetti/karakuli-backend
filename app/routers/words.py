from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import User, Word
from app.schemas.word import WordCreate
from app.scrapper import words

api = APIRouter(tags=["Words"], prefix="/words")


@api.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def add(
        word: WordCreate,
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user())
):
    # Todo Add some checks before adding the word? mb ЛЕВЕНШТАЙН ДЫСТАНС
    word = Word(**word.dict(), user_id=current_user.id)
    session.add(word)
    await session.commit()
    await session.refresh(word)

    return word


@api.post(
    "/parse",
    status_code=status.HTTP_200_OK,
)
async def parse(
        session: AsyncSession = Depends(get_db_session),
):
    if await Word.get_by_id(session, 200) is not None:  # Todo remove this retarded if
        return "Already parsed"
    else:
        gen = words()
        for _ in range(50):
            w = next(gen)
            session.add(Word(**w, user_id=0))
            await session.commit()

    return "Done"
