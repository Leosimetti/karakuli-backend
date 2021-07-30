from sqlalchemy import Column, Integer, String

from app.models import Base


class Radical(Base):
    __tablename__ = 'radicals'

    id = Column(Integer, primary_key=True)

    strokes = Column(Integer, nullable=False)
    meaning = Column(String, nullable=False)
