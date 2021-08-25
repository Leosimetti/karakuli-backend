from sqlalchemy import Column, ForeignKey, Integer, Text, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.lessons import Lesson


# Todo @todo dehardcode table references
class StudyItem(Base):
    __tablename__ = "studyitems"

    list_id = Column(Integer, ForeignKey("studylists.id"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey(Lesson.id), primary_key=True)

    position = Column(Integer, nullable=False)
    note = Column(Text())

    lesson = relationship(Lesson)  # Todo @todo check if this is useless

    @staticmethod
    async def get(session: AsyncSession, list_id: int, lesson_id: int):
        result = await session.execute(
            select(StudyItem).where(
                and_(StudyItem.list_id == list_id, StudyItem.lesson_id == lesson_id)
            )
        )

        return result.scalar()
