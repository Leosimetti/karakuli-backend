from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.lessons.example import Example

_table_name = 'grammars'

association_examples = Table('grammar_to_examples', Base.metadata,
                             Column('grammar', ForeignKey(_table_name + ".id"), primary_key=True),
                             Column('example', ForeignKey(Example.id), primary_key=True)
                             )


class Grammar(Base):
    __tablename__ = _table_name

    id = Column(Integer, primary_key=True)
    examples = relationship(Example, secondary=association_examples)
