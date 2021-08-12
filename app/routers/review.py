import datetime

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import User, Review, Word, Lesson
from app.models.review import ReviewType
from app.depends import get_db_session, get_current_user
from app.schemas.review import ReviewSubmit
import app.srs as srs

api = APIRouter(tags=["Review"], prefix="/reviews")


@api.post(
    "/{lesson_id}",
    status_code=status.HTTP_201_CREATED,
)
async def review_word(
        lesson_id: int,
        review: ReviewSubmit,
        current_user: User = Depends(get_current_user("reviews")),
        session: AsyncSession = Depends(get_db_session)
):
    rev: Review = await Review.get(session, current_user.id, lesson_id, review.review_type)
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
async def add_lesson_to_review(
        current_user: User = Depends(get_current_user("reviews")),
        session: AsyncSession = Depends(get_db_session),
        lessons: List[int] = Query(None, alias="lesson_id")
):
    # Todo mb optimize the query?

    # removing duplicates
    if lessons is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='No lessons to add.'
        )
    lessons = set(lessons)
    already_added = []
    successfully_added = []

    tmp = await session.execute(select(Lesson.id).where(Lesson.id.in_(lessons)))

    existing = tmp.scalars().all()
    non_existent = lessons.difference(set(existing))

    for l in existing:
        for r_type in ReviewType._member_map_:  # Todo find a better way to access values of enum
            _, new_time = srs.correct_answer(0, False)  # Todo make it look less stupid?
            new_time = datetime.datetime.timestamp(new_time)
            review = Review(user_id=current_user.id,
                            lesson_id=l,
                            type=r_type,
                            srs_stage=0,
                            total_correct=1,
                            total_incorrect=0,
                            review_date=new_time)

            if await Review.get(session, current_user.id, l, r_type):
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
        session: AsyncSession = Depends(get_db_session),
        current_user: User = Depends(get_current_user("reviews", "reviews.lesson")),
):
    # Todo maybe somehow add the study list note????
    now = datetime.datetime.now()
    # Todo check of doing a db query is more efficient
    filter_func = lambda x: x.review_date <= datetime.datetime.timestamp(now)
    result = list(filter(filter_func, current_user.reviews))
    result_with_content = list(map(lambda x: Lesson.get_content(session, x.id), result))
    return result_with_content
