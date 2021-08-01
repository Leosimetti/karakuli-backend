from enum import Enum as _Enum, auto

from sqlalchemy import Column, Integer, and_
from sqlalchemy import TIMESTAMP, Enum, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.lessons.lesson import Lesson


class ReviewType(_Enum):
    meaning = auto()
    reading = auto()
    # spelling = auto() # Todo make these types available
    # listening = auto()
    # pronunciation = auto()


# Todo dehardcode table references
class Review(Base):
    __tablename__ = 'reviews'

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    lesson_id = Column(Integer, ForeignKey(Lesson.id), primary_key=True)
    type = Column(Enum(ReviewType), primary_key=True)

    srs_stage = Column(Integer, nullable=False)
    total_correct = Column(Integer, nullable=False)
    total_incorrect = Column(Integer, nullable=False)
    review_date = Column(TIMESTAMP, index=True, nullable=False)

    user = relationship("User", back_populates="reviews")
    lesson = relationship(Lesson)

    @staticmethod
    async def get(session: AsyncSession, user_id: int, lesson_id: int, review_type: ReviewType):
        result = await session.execute(
            select(Review).where(
                and_(
                    Review.user_id == user_id,
                    Review.lesson_id == lesson_id,
                    Review.type == review_type
                )
            )
        )

        return result.scalar()
