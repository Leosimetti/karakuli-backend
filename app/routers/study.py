from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, StudyList, Word, StudyItem
from app.schemas.word import WordList
from app.depends import get_db_session, get_current_user

api = APIRouter(tags=["Study"], prefix="/study")


@api.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def add_word_to_study_list(
        word: WordList,
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(get_db_session),
):
    if not await Word.get_by_id(session, word.word_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Word not found.'
        )

    study_list = await StudyList.get_by_id(session, word.list_id, "user", "items")
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

    item = StudyItem(list_id=word.list_id,
                     word_id=word.word_id,
                     note=word.note
                     )
    sas = await StudyItem.get(session, word.list_id, word.word_id)
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

    await session.commit()  # Todo check if the commit should be after all adds
    return item


# Todo make it possible to update item note and position

@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_n_current_user_study_items(
        n: int,
        session: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user()),
):
    return await StudyList.get_n_new_words(session, user.current_list_id, user.id, n)  # tODO take user into account
