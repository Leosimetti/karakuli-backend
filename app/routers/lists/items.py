from fastapi import status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, StudyList, Lesson, StudyItem
from app.schemas.word import LessonInList
from app.depends import get_db_session, get_current_user
from app.routers.lists import api


# Todo create a Depends() for extracting the id

@api.get("/{list_id_or_name}/items",
         status_code=status.HTTP_200_OK,
         responses={
             404: {"detail": "List not found."},
         }
         )
async def get_list_items(
        list_id_or_name: str,
        # _: User = Depends(get_current_user()),
        session: AsyncSession = Depends(get_db_session),
):
    # Todo compress this duplicate code into a separate function or depends or class method
    if list_id_or_name.isnumeric():
        study_list = await StudyList.get_by_id(session, list_id_or_name, "user", "items")
    else:
        study_list = await StudyList.get_by_name(session, list_id_or_name, "user", "items")

    if not study_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='List not found.'
        )

    lesson_ids = list(map(lambda item: item.lesson_id, study_list.items))
    lessons = [await Lesson.getContent(session, l_id) for l_id in lesson_ids]
    # Todo mb append notes as positions are already reflected in the order of items

    return lessons


# Todo somehow make responses refer to actual responses instead of copy-paste
@api.post(
    "/{list_id_or_name}/items",
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {"detail": "You cannot add to this list."},
        404: {"detail": "List not found./Lesson not found."},
        409: {"detail": "This item is already in the list."},
    }
)
async def add_item_to_study_list(
        list_id_or_name: str,
        lesson: LessonInList,
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(get_db_session),
):
    if not await Lesson.get_by_id(session, lesson.lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Lesson not found.'
        )

    # Todo compress this duplicate code into a separate function or depends or class method
    if list_id_or_name.isnumeric():
        study_list = await StudyList.get_by_id(session, list_id_or_name, "user", "items")
    else:
        study_list = await StudyList.get_by_name(session, list_id_or_name, "user", "items")

    if not study_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='List not found.'
        )
    if study_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You cannot add to this list.'
        )

    item = StudyItem(list_id=study_list.id,
                     lesson_id=lesson.lesson_id,
                     note=lesson.note
                     )
    sas = await StudyItem.get(session, study_list.id, lesson.lesson_id)
    if sas:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='This item is already in the list.'
        )
    else:
        session.add(item)
        if lesson.position:
            study_list.items.insert(lesson.position, item)
        else:
            study_list.items.append(item)

    await session.commit()
    return item


# Todo Check if changing positions can behave in strange ways
# Todo create a Depends() for extracting the id
@api.put(
    "/{list_id_or_name}/items",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"detail": "You cannot edit this list."},
        404: {"detail": "List not found./Item not found."},
        409: {"detail": "This item is already in the list."},
        422: {"detail": "No information to update provided."},
    }
)
async def update_item_information_in_list(
        list_id_or_name: str,
        lesson: LessonInList,
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(get_db_session),
):
    if (not lesson.note) and (not lesson.position):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='No information to update provided.'
        )

    # Todo compress this duplicate code into a separate function or depends or class method
    if list_id_or_name.isnumeric():
        study_list = await StudyList.get_by_id(session, list_id_or_name, "user", "items")
    else:
        study_list = await StudyList.get_by_name(session, list_id_or_name, "user", "items")

    if not study_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='List not found.'
        )

    if study_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You cannot edit this list.'
        )

    item = await StudyItem.get(session, study_list.id, lesson.lesson_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found.'
        )

    item.note = lesson.note if lesson.note else item.note

    if lesson.position is not None:
        study_list.items.remove(item)
        study_list.items.insert(lesson.position - 1, item)

    await session.commit()
    await session.refresh(item)
    return item
