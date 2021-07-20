from sqlalchemy import Column, Integer, DATETIME, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.models import BaseModel, Base
from enum import Enum as _Enum, auto


class ReviewType(_Enum):
    meaning = auto()
    reading = auto()
    spelling = auto()
    listening = auto()
    pronunciation = auto()


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
    review_date = Column(DATETIME)

    user = relationship("User", back_populates="reviews")
    word = relationship("Word")
