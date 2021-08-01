from sqlalchemy import Column, Integer, String

from app.models import Base
from app.models.lessons.types.base_type import BaseType


class Radical(Base, BaseType):
    __tablename__ = 'radicals'

    # id = Column(Integer, primary_key=True)

    radical = Column(String(2), nullable=False, unique=True)
    meaning = Column(String, nullable=False)
    strokes = Column(Integer, nullable=False)
