from sqlalchemy import Column, Integer, Table, ForeignKey, JSON, String
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.lessons.example import Example
from app.models.lessons.types.base_type import BaseType

_table_name = 'grammars'

association_examples = Table('grammar_to_examples', Base.metadata,
                             Column('grammar', ForeignKey(_table_name + ".lesson_id"), primary_key=True),
                             Column('example', ForeignKey(Example.id), primary_key=True),
                             Column("meta", JSON)
                             )


class Grammar(Base, BaseType):
    __tablename__ = _table_name

    description = Column(String, nullable=False)
    links = Column(JSON, nullable=True)
    meta = Column(JSON, nullable=True)

    examples = relationship(Example, secondary=association_examples)
