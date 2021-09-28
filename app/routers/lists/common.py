from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import StudyList, User

api = APIRouter(tags=["Study List"], prefix="")


# Todo @todo add a way to change user' current list
@api.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"detail": "This name is already taken."},
    },
)
async def create_study_list(
    name: str = Query(..., regex=r"\D"),
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user()),
):
    if await StudyList.get_by_name(session, name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This name is already taken."
        )

    study_list = StudyList(name=name, user_id=current_user.id)
    session.add(study_list)
    await session.commit()
    await session.refresh(study_list)

    return study_list


# Todo @todo create a Depends() for extracting the id
@api.get(
    "/{list_id_or_name}",
    responses={
        404: {"detail": "List not found."},
    },
)
async def get_list_by_id_or_name(
    list_id_or_name: str,
    session: AsyncSession = Depends(get_db_session),
):

    if list_id_or_name.isnumeric():
        result = await StudyList.get_by_id(session, list_id_or_name)
    else:
        result = await StudyList.get_by_name(session, list_id_or_name)

    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found."
        )
