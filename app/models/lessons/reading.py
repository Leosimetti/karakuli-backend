from sqlalchemy import Column, Integer, String

from app.models import Base


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True)
    reading = Column(String, nullable=False, unique=True)
