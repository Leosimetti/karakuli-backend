from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.srs as srs
from app.depends import get_current_user, get_db_session
from app.models import Lesson, Review, User
from app.models.review import LESSON_TO_REVIEW_MAPPING, ReviewType
from app.schemas.review import ReviewSubmit

api = APIRouter(tags=["Review"], prefix="/reviews")


@api.post(
    "/{lesson_id}",
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {"detail": "This item is not available for review yet."},
        404: {"detail": "Review not found."},
    },
)
async def review_item(
    lesson_id: int,
    review: ReviewSubmit,
    current_user: User = Depends(get_current_user("reviews")),
    session: AsyncSession = Depends(get_db_session),
):
    rev: Review = await Review.get(
        session, current_user.id, lesson_id, review.review_type
    )
    if not rev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found."
        )

    if rev.review_date > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This item is not available for review yet.",
        )

    if review.incorrect_answers:
        new_stage, new_date = srs.incorrect_answer(
            rev.srs_stage, review.incorrect_answers, False
        )
        rev.total_incorrect += review.incorrect_answers
    else:
        new_stage, new_date = srs.correct_answer(rev.srs_stage, False)

    rev.srs_stage = new_stage
    rev.review_date = new_date
    rev.total_correct += 1  # Todo @todo maybe add a limit to incorrect answers, in which case it will be 0

    await session.commit()
    await session.refresh(rev)

    return rev


@api.get(
    "/{lesson_id}",
    status_code=status.HTTP_200_OK,
    responses={
        403: {"detail": "This item does not belong to the current user."},
        404: {"detail": "Review not found."},
    },
)
async def get_reviews_for_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user("reviews")),
    session: AsyncSession = Depends(get_db_session),
):
    reviews = []
    for (
        r_type
    ) in (
        ReviewType._member_map_
    ):
        rev: Review = await Review.get(session, current_user.id, lesson_id, r_type)

        # Todo @todo check if this is actually necessary
        if rev:
            if rev.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This item does not belong to the current user.",
                )
            else:
                reviews.append(rev)

    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found."
        )

    return reviews


@api.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={422: {"detail": "No lessons to add."}},
)
async def add_lesson_to_review(
    current_user: User = Depends(get_current_user("reviews")),
    session: AsyncSession = Depends(get_db_session),
    lessons: List[int] = Query(None, alias="lesson_id"),
):
    # Todo @todo mb optimize the query?

    if lessons is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No lessons to add.",
        )
    lessons = set(lessons)  # removing duplicates
    already_added = []
    successfully_added = []

    tmp = await session.execute(select(Lesson.id).where(Lesson.id.in_(lessons)))

    existing = tmp.scalars().all()
    non_existent = lessons.difference(set(existing))

    for lesson_id in existing:
        lesson_type = (await Lesson.get_by_id(session, lesson_id)).type
        review_types = LESSON_TO_REVIEW_MAPPING[lesson_type]

        # Creating necessary review types for the current lesson
        for (
            r_type
        ) in review_types:
            _, new_time = srs.correct_answer(
                0, False
            )  # Todo @todo make it look less stupid?
            # new_time = datetime.datetime.timestamp(new_time)
            review = Review(
                user_id=current_user.id,
                lesson_id=lesson_id,
                type=r_type,
                srs_stage=0,
                total_correct=1,
                total_incorrect=0,
                review_date=new_time,
            )

            existing_review = await Review.get(
                session, current_user.id, lesson_id, r_type
            )
            if existing_review:
                already_added.append(existing_review)
            else:
                session.add(review)
                successfully_added.append(review)

    await session.commit()
    # Todo @todo check if there is a better way to do batch adds
    return {
        "added": successfully_added,
        "already_added": already_added,
        "non_existent": non_existent,
    }


@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_due_user_reviews(
    limit: Optional[int] = None,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user("reviews", "reviews.lesson")),
):
    # Todo @todo only give reviews that are from the current list???? Allow users to combine lists?
    # Todo @todo maybe somehow add the study list note????
    now = datetime.now()
    # now = datetime.datetime.timestamp(now)
    # Todo @todo check if this is ok to do
    reviews = current_user.reviews[:limit] if limit else current_user.reviews
    # Todo @todo check of doing a db query is more efficient
    filter_func = lambda x: x.review_date <= now
    result = list(filter(filter_func, reviews))
    result_with_content = [
        await Lesson.get_content(session, x.lesson_id) for x in result
    ]
    return result_with_content
