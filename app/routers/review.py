import datetime

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import User, Review, Word
from app.depends import get_db_session, get_current_user

api = APIRouter(tags=["Review"], prefix="/reviews")

# @api.post(
#     "",
#     status_code=status.HTTP_201_CREATED,
# )
# async def add_word_to_study_list(
#         list_id: int,
#         position: Optional[int] = None,
#         words: int = Query(None, alias="word_id"),
#         current_user: User = Depends(get_current_user()),
#         session: AsyncSession = Depends(get_db_session),
# ):
#     if not words:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail='No words provided.'
#         )
#
#     # removing duplicates
#     words = set(words)
#     already_added = []
#     successfully_added = []
#
#     tmp = await session.execute(select(Word.id).where(Word.id.in_(words)))
#
#     existing = tmp.scalars().all()
#     non_existent = words.difference(set(existing))
#
#     # Todo check if list belongs to the user
#
#     for w_id in existing:
#         item = StudyItem(list_id=current_user.current_list_id,
#                          word_id=w_id
#                          )
#         sas = await StudyItem.get(session, list_id, w_id)
#         if sas:
#             already_added.append(item)
#         else:
#             study_list = await StudyList.get_by_id(session, list_id, "items")
#             session.add(item)
#             if position:
#                 study_list.items.insert(position, item)
#             else:
#                 study_list.items.append(item)
#             successfully_added.append(item)
#
#     await session.commit()  # Todo check if the commit should be after all adds
#     return {
#         "added": successfully_added,
#         "already_added": already_added,
#         "non_existent": non_existent
#     }



# @api.post(
#     "",
#     status_code=status.HTTP_201_CREATED,
# )
# async def add_word_to_review(
#         current_user: User = Depends(get_current_user("reviews")),
#         session: AsyncSession = Depends(get_db_session),
#         words: List[int] = Query(None, alias="word_id")
# ):
#     # Todo mb optimize the query?
#
#     # removing duplicates
#     words = set(words)
#     already_added = []
#     successfully_added = []
#
#     tmp = await session.execute(select(Word.id).where(Word.id.in_(words)))
#
#     existing = tmp.scalars().all()
#     non_existent = words.difference(set(existing))
#
#     from app.models.review import ReviewType
#     for w_id in existing:
#         for r_type in ReviewType._member_map_:  # Todo find a better way to access values of enum
#             review = Review(user_id=current_user.id,
#                             word_id=w_id,
#                             type=r_type,
#                             srs_stage=0,
#                             total_correct=0,
#                             total_incorrect=0,
#                             review_date=datetime.datetime(year=10, month=10, day=10))
#             if await Review.get(session, current_user.id, w_id, r_type):
#                 already_added.append(review)
#             else:
#                 session.add(review) # Todo fix that only one type is added
#                 successfully_added.append(review)
#
#     await session.commit()
#     return {
#         "added": successfully_added,
#         "already_added": already_added,
#         "non_existent": non_existent
#     }


@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
def list_current_user_reviews(
        current_user: User = Depends(get_current_user("reviews")),
):
    return current_user.reviews
