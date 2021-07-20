from sqlalchemy import Column, Integer, String, JSON
from app.models import BaseModel, Base


# Todo make it the same in the front
class Word(Base, BaseModel):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    meaning = Column(String(length=100), nullable=False)
    reading = Column(String(length=100), unique=True, nullable=False)
    kanji = Column(String(length=60), nullable=False)
    example = Column(String(length=100), unique=True, nullable=True)
    meta = Column(JSON, nullable=True)
