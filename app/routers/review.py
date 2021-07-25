import datetime

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import User, Review, Word
from app.models.review import ReviewType
from app.depends import get_db_session, get_current_user
from app.schemas.review import ReviewSubmit
import app.srs as srs

api = APIRouter(tags=["Review"], prefix="/reviews")


@api.post(
    "/{word_id}",
    status_code=status.HTTP_201_CREATED,
)
async def review_word(
        word_id: int,
        review: ReviewSubmit,
        current_user: User = Depends(get_current_user("reviews")),
        session: AsyncSession = Depends(get_db_session)
):
    rev: Review = await Review.get(session, current_user.id, word_id, review.review_type)
    if not rev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found.'
        )

    if rev.review_date > datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='This item is not available for review yet.'
        )

    if review.incorrect_answers:
        new_stage, new_date = srs.incorrect_answer(rev.srs_stage, review.incorrect_answers, False)
        rev.total_incorrect += review.incorrect_answers
    else:
        new_stage, new_date = srs.correct_answer(rev.srs_stage, False)

    rev.srs_stage = new_stage
    rev.review_date = new_date
    rev.total_correct += 1  # Todo maybe add a limit to incorrect answers, in which case it will be 0

    await session.commit()
    await session.refresh(rev)

    return rev


@api.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def add_word_to_review(
        current_user: User = Depends(get_current_user("reviews")),
        session: AsyncSession = Depends(get_db_session),
        words: List[int] = Query(None, alias="word_id")
):
    # Todo mb optimize the query?

    # removing duplicates
    words = set(words)
    already_added = []
    successfully_added = []

    tmp = await session.execute(select(Word.id).where(Word.id.in_(words)))

    existing = tmp.scalars().all()
    non_existent = words.difference(set(existing))

    for w_id in existing:
        for r_type in ReviewType._member_map_:  # Todo find a better way to access values of enum
            _, new_time = srs.correct_answer(0, False)  # Todo make it look less stupid?
            review = Review(user_id=current_user.id,
                            word_id=w_id,
                            type=r_type,
                            srs_stage=0,
                            total_correct=1,
                            total_incorrect=0,
                            review_date=new_time)

            if await Review.get(session, current_user.id, w_id, r_type):
                already_added.append(review)
            else:
                session.add(review)
                successfully_added.append(review)

    await session.commit()
    # Todo check if there is a better way to do batch adds
    return {
        "added": successfully_added,
        "already_added": already_added,
        "non_existent": non_existent
    }


@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
def list_current_user_reviews(
        current_user: User = Depends(get_current_user("reviews", "reviews.word")),
):
    # Todo maybe somehow add the study list note????
    filter_func = lambda x: x.review_date <= datetime.datetime.now()
    result = list(filter(filter_func, current_user.reviews))
    return result
