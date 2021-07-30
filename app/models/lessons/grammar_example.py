from sqlalchemy import Column, Integer

from app.models import Base


class GrammarExample(Base):
    __tablename__ = 'grammar_examples'

    id = Column(Integer, primary_key=True)
