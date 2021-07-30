from sqlalchemy import Column, Integer, String

from app.models import Base


class Example(Base):
    __tablename__ = 'examples'

    id = Column(Integer, primary_key=True)
    sentence = Column(String, nullable=False)