from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.models import Base

class Kanji(Base):
    __tablename__ = 'kanjis'

    id = Column(Integer, primary_key=True)
