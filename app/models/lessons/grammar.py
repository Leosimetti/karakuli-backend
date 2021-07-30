from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.models import Base

class Grammar(Base):
    __tablename__ = 'grammars'

    id = Column(Integer, primary_key=True)
