from fastapi import APIRouter, Depends, status
from sqlalchemy import select, except_
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends import get_current_user, get_db_session
from app.models import User, StudyItem, Review, Lesson

api = APIRouter(tags=["Study"], prefix="/study")


@api.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_n_current_user_study_items(
        n: int,
        session: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user()),
):
    # Todo @todo find out why negatives crash; add a check for them

    study_list_items = select(StudyItem.lesson_id).where(StudyItem.list_id == user.current_list_id)
    user_reviews = select(Review.lesson_id).where(Review.user_id == user.id)
    new_study_items = await session.execute(except_(study_list_items, user_reviews))
    lesson_ids = new_study_items.scalars().all()

    lesson_objects = select(StudyItem.lesson_id, StudyItem.position).where(
        StudyItem.lesson_id.in_(lesson_ids)
    )
    lessons_filtered = await session.execute(lesson_objects.order_by(StudyItem.position).limit(n))
    lesson_ids = lessons_filtered.scalars().all()

    lessons = [await Lesson.get_content(session, l_id) for l_id in lesson_ids]
    return lessons
