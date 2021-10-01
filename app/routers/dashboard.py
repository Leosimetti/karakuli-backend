from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, except_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.depends import get_current_user, get_db_session
from app.models import User, StudyItem, Review

api = APIRouter(tags=["Dashboard"], prefix="/dashboard")


@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def see_amount_of_available_items(
        session: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user("reviews")),
):
    # TOdo remove this gavno
    study_list_items = select(StudyItem.lesson_id).where(StudyItem.list_id == user.current_list_id)
    user_reviews = select(Review.lesson_id).where(Review.user_id == user.id)
    new_study_items = await session.execute(except_(study_list_items, user_reviews))
    amount_of_lessons = len(new_study_items.scalars().all())

    now = datetime.now()
    reviews = user.reviews
    filter_func = lambda x: x.review_date <= now
    amount_of_reviews = len(list(filter(filter_func, reviews)))

    return {"lessons": amount_of_lessons, "reviews": amount_of_reviews}
