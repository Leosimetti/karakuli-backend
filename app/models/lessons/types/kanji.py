from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.lessons.reading import Reading
from app.models.lessons.types.base_type import BaseType
from app.models.lessons.types.radical import Radical

_table_name = "kanjis"

association_radicals = Table(
    "kanji_to_radicals",
    Base.metadata,
    Column("kanji", ForeignKey(_table_name + ".lesson_id"), primary_key=True),
    Column("radical", ForeignKey(Radical.lesson_id), primary_key=True),
)

association_readings = Table(
    "kanji_to_readings",
    Base.metadata,
    Column("kanji", ForeignKey(_table_name + ".lesson_id"), primary_key=True),
    Column("reading", ForeignKey(Reading.id), primary_key=True),
)


class Kanji(Base, BaseType):
    __tablename__ = _table_name

    character = Column(
        String, nullable=False, unique=True
    )  # Todo @todo add length constraint?
    meaning = Column(String, nullable=False)
    strokes = Column(Integer, nullable=False)
    joyo_level = Column(String)
    jlpt_level = Column(String)
    links = Column(JSON, nullable=True)
    reading = Column(String, nullable=False)

    radicals = relationship(Radical, secondary=association_radicals)
    readings = relationship(Reading, secondary=association_readings)

    @classmethod
    async def get_by_kanji(cls, session: AsyncSession, kanji: str):
        query = select(Kanji).where(Kanji.character == kanji)
        result = await session.execute(query)

        return result.scalar()
