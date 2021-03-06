from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import StudyList, User
from app.schemas.study_list import StudyListCreate

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
        new_list: StudyListCreate,
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user()),
):
    if await StudyList.get_by_name(session, new_list.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This name is already taken."
        )

    study_list = StudyList(name=new_list.name, user_id=current_user.id, img_url=new_list.img_url, description=new_list.description)
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


@api.post(
    "/{list_id_or_name}",
    responses={
        404: {"detail": "List not found."},
    },
)
async def choose_list_by_id_or_name(
        list_id_or_name: str,
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user()),
):
    if list_id_or_name.isnumeric():
        result = await StudyList.get_by_id(session, list_id_or_name)
    else:
        result = await StudyList.get_by_name(session, list_id_or_name)

    if result:
        current_user.current_list_id = result.id
        await session.commit()
        return "All good"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found."
        )


@api.get(
    "/"
)
async def get_available_lists(
        session: AsyncSession = Depends(get_db_session),
):
    lists = await session.execute(select(StudyList))

    return lists.scalars().all()
