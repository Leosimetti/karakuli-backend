from fastapi import APIRouter, status, Depends, HTTPException

from app.models import User, Word, StudyList
from sqlalchemy.ext.asyncio import AsyncSession
from app.depends import get_current_user, get_db_session

from app.scrapper import words

api = APIRouter(tags=["Words"], prefix="/words")


@api.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def add(
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user()),
):
    if await Word.get_by_id(session, 200) is not None:
        return "Already parsed"
    else:
        for w in words():
            session.add(Word(**w))
            await session.commit()

    return "Done"


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
            session.add(Word(**w))
            await session.commit()

    return "Done"


@api.post(
    "/create_list",
    status_code=status.HTTP_200_OK,
)
async def create_study_list(
        name: str,
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user()),
):
    if await StudyList.get_by_name(session, name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='This name is already taken.'
        )

    study_list = StudyList(name=name, user_id=current_user.id)
    session.add(study_list)
    await session.commit()
    await session.refresh(study_list)

    return study_list
