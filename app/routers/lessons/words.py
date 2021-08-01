from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import User, Word
from app.schemas.word import WordCreate
from app.scrapper import kanji

api = APIRouter(tags=["Words"], prefix="/words")


@api.post(
    "",
    status_code=status.HTTP_200_OK,
)
async def add(
        word: WordCreate,
        session: AsyncSession = Depends(get_db_session),
        _: User = Depends(get_current_user())
):
    # Todo Add some checks before adding the word? mb ЛЕВЕНШТАЙН ДЫСТАНС
    word = await Word.create(session, word)

    return word
