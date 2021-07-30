from sqlalchemy import Column, Integer

from app.models import Base


class WordReading(Base):
    __tablename__ = 'word_readings'

    id = Column(Integer, primary_key=True)
