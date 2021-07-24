from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, StudyList, Word, StudyItem
from app.schemas.word import WordInList
from app.depends import get_db_session, get_current_user
from app.routers.lists import api


# Todo create a Depends() for extracting the id
@api.post(
    "{list_id_or_name}/words",
    status_code=status.HTTP_201_CREATED,
)
async def add_word_to_study_list(
        list_id_or_name: str,
        word: WordInList,
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(get_db_session),
):
    if not await Word.get_by_id(session, word.word_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Word not found.'
        )

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
                     word_id=word.word_id,
                     note=word.note
                     )
    sas = await StudyItem.get(session, study_list.id, word.word_id)
    if sas:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='This item is already in the list.'
        )
    else:
        session.add(item)
        if word.position:
            study_list.items.insert(word.position, item)
        else:
            study_list.items.append(item)

    await session.commit()
    return item


# Todo Check if changing positions can behave in strange ways
# Todo create a Depends() for extracting the id
@api.put(
    "/{list_id_or_name}/words",
    status_code=status.HTTP_201_CREATED,
)
async def update_word_information_in_list(
        list_id_or_name: str,
        word: WordInList,
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(get_db_session),
):
    if (not word.note) and (not word.position):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='No information to update provided.'
        )

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

    item = await StudyItem.get(session, study_list.id, word.word_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found.'
        )

    item.note = word.note if word.note else item.note

    if word.position:
        study_list.items.remove(item)
        study_list.items.insert(word.position, item)

    await session.commit()
    await session.refresh(item)
    return item
