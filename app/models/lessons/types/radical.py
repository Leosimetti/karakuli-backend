from sqlalchemy import Column, Integer, String

from app.models import Base
from app.models.lessons.types.base_type import BaseType


class Radical(Base, BaseType):
    __tablename__ = 'radicals'

    radical = Column(String(2), nullable=False, unique=True) # Todo check why length is not enforced
    meaning = Column(String, nullable=False)
    strokes = Column(Integer, nullable=False)
