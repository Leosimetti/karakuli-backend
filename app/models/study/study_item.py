from sqlalchemy import Column, Integer, ForeignKey, Text, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

from app.models import Base


class StudyItem(Base):
    __tablename__ = 'studyitems'

    # id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("studylists.id"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), primary_key=True)

    position = Column(Integer, nullable=False)
    note = Column(Text())

    lesson = relationship("Lesson")

    @staticmethod
    async def get(session: AsyncSession, list_id: int, lesson_id: int):
        result = await session.execute(
            select(StudyItem).where(
                and_(
                    StudyItem.list_id == list_id,
                    StudyItem.lesson_id == lesson_id)
            )
        )

        return result.scalar()