from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.models import BaseModel, Base


# Todo make it the same in the front
class Word(Base, BaseModel):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    meaning = Column(String(length=100), nullable=False)
    readings = Column(String(length=100), nullable=False)  # Todo find a better way to store reading
    kanji = Column(String(length=60), nullable=False)
    example = Column(String(length=100), nullable=True)
    meta = Column(JSON, nullable=True)

    user = relationship("User", back_populates="added_words")
