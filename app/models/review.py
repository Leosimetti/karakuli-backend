from enum import Enum as _Enum, auto

from sqlalchemy import Column, Integer
from sqlalchemy import DATETIME, Enum, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from app.models import Base


class ReviewType(_Enum):
    meaning = auto()
    reading = auto()
    # spelling = auto() # Todo make these types available
    # listening = auto()
    # pronunciation = auto()


# Todo make it the same in the front
class Review(Base):
    __tablename__ = 'reviews'

    # id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
    type = Column(Enum(ReviewType), nullable=False, primary_key=True)

    srs_stage = Column(Integer, nullable=False)
    total_correct = Column(Integer, nullable=False)
    total_incorrect = Column(Integer, nullable=False)
    review_date = Column(DATETIME, index=True)

    user = relationship("User", back_populates="reviews")
    word = relationship("Word")

    @staticmethod
    async def get(session: AsyncSession, user_id: int, word_id: int, review_type: ReviewType):
        result = await session.execute(
            select(Review).where(
                Review.user_id == user_id
                and Review.word_id == word_id
                and Review.type == review_type
            )
        )

        return result.scalar()
