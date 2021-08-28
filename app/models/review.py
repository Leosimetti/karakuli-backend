from enum import Enum as _Enum

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from app.models import Base, BaseModel
from app.models.lessons.lesson import Lesson, LessonType


class ReviewType(_Enum):
    # Todo @todo Add a constraint for review types to lesson types via the mapping below
    meaning = "meaning"
    reading = "reading"
    other = "other"
    # spelling = auto() # Todo @todo make these types available in a proper way
    # listening = auto()
    # pronunciation = auto()


LESSON_TO_REVIEW_MAPPING = {
    LessonType.kanji: [ReviewType.meaning, ReviewType.reading],
    LessonType.word: [ReviewType.meaning, ReviewType.reading],
    LessonType.radical: [ReviewType.meaning],
    LessonType.grammar: [ReviewType.other],
}


# Todo @todo dehardcode table references
class Review(Base):
    __tablename__ = "reviews"

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
    async def get(
        session: AsyncSession, user_id: int, lesson_id: int, review_type: ReviewType
    ):
        # Todo @todo add boundary checking for ids
        result = await session.execute(
            select(Review).where(
                and_(
                    Review.user_id == user_id,
                    Review.lesson_id == lesson_id,
                    Review.type == review_type,
                )
            )
        )

        return result.scalar()
