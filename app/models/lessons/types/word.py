from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.lessons.types.kanji import Kanji
from app.models.lessons.example import Example
from app.models.lessons.reading import Reading

_table_name = 'words'

association_readings = Table('word_to_readings', Base.metadata,
                             Column('word', ForeignKey(_table_name + ".id"), primary_key=True),
                             Column('reading', ForeignKey(Reading.id), primary_key=True),
                             Column('position', Integer, primary_key=True)
                             )

association_examples = Table('word_to_examples', Base.metadata,
                             Column('word', ForeignKey(_table_name + ".id"), primary_key=True),
                             Column('example', ForeignKey(Example.id), primary_key=True)
                             )

association_kanjis = Table('word_to_kanjis', Base.metadata,
                           Column('word', ForeignKey(_table_name + ".id"), primary_key=True),
                           Column('kanji', ForeignKey(Kanji.id), primary_key=True)
                           )


class Word(Base):
    __tablename__ = _table_name

    id = Column(Integer, primary_key=True)

    readings = relationship(Reading, secondary=association_readings)
    examples = relationship(Example, secondary=association_examples)
    kanjis = relationship(Kanji, secondary=association_kanjis)

# from sqlalchemy import Column, Integer, String, JSON, ForeignKey
# from sqlalchemy.orm import relationship
#
# from app.models import BaseModel, Base

# Todo make it the same in the front
# class Word(Base, BaseModel):
#     __tablename__ = 'words'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), index=True)
#     meaning = Column(String(length=100), nullable=False)
#     readings = Column(String(length=100), nullable=False)  # Todo find a better way to store reading
#     kanji = Column(String(length=60), nullable=False)
#     example = Column(String(length=100), nullable=True)
#     meta = Column(JSON, nullable=True)
#
#     user = relationship("User", back_populates="added_words")
