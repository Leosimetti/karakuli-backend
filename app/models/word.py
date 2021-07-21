from sqlalchemy import Column, Integer, String, JSON
from app.models import BaseModel, Base


# Todo make it the same in the front
class Word(Base, BaseModel):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    meaning = Column(String(length=100), nullable=False)
    readings = Column(String(length=100), nullable=False)
    kanji = Column(String(length=60), nullable=False)
    example = Column(String(length=100), nullable=True)
    meta = Column(JSON, nullable=True)  # Todo maybe change to json
