from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, backref

from app.models import Base


class Radical(Base):
    __tablename__ = 'radicals'

    id = Column(Integer, primary_key=True)
