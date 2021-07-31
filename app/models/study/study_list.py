from sqlalchemy import Column, Integer, Boolean, String, Text, except_
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.orderinglist import ordering_list, count_from_1

from app.models import Base, BaseModel

from app.models.study.study_item import StudyItem
from app.models.lessons import Lesson
from app.models.review import Review


# Todo dehardcode table references
class StudyList(Base, BaseModel):
    __tablename__ = 'studylists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    approved = Column(Boolean, default=False)

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text())

    user = relationship("User", back_populates="created_study_lists")
    items = relationship(StudyItem, order_by=StudyItem.position,
                         collection_class=ordering_list('position', ordering_func=count_from_1))

    @staticmethod
    async def get_n_new_words(session: AsyncSession, list_id: int, user_id: int, n: int):
        # Todo find out why negatives crash
        select_items = select(StudyItem.lesson_id).where(StudyItem.list_id == list_id)
        select_reviews = select(Review.lesson_id).where(Review.user_id == user_id)
        removed_intersection = except_(select_items, select_reviews)

        tmp = await session.execute(removed_intersection)
        lesson_ids = tmp.scalars().all()

        lessons_appropriate = select(StudyItem.lesson_id, StudyItem.position).where(StudyItem.lesson_id.in_(lesson_ids))
        lessons_filtered = lessons_appropriate.order_by(StudyItem.position).limit(n)

        tmp = await session.execute(lessons_filtered)
        lesson_ids = tmp.scalars().all()

        result = [await Lesson.getContent(session, l_id) for l_id in lesson_ids]

        return result

    @staticmethod
    async def get_by_name(session: AsyncSession, name: str, *fields_to_load):
        query = select(StudyList).where(
            StudyList.name == name,
        )

        if fields_to_load:
            for field in fields_to_load:
                query = query.options(selectinload(field))

        result = await session.execute(query)
        return result.scalar()
