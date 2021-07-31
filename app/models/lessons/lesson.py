from enum import Enum as _Enum

from sqlalchemy import Column, Integer, CheckConstraint
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, selectinload, backref

from app.models import Base, BaseModel
from app.models.lessons.types import Kanji, Radical, Word, Grammar
from app.models.lessons.types.base_type import BaseType


class LessonType(_Enum):
    radical = "rad"
    kanji = "kan"
    word = "wor"
    grammar = "grm"


mapping = {
    LessonType.radical: Radical,
    LessonType.kanji: Kanji,
    LessonType.word: Word,
    LessonType.grammar: Grammar,
}


class Lesson(Base, BaseModel):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(LessonType), nullable=False)

    # item = relationship(BaseType, back_populates="lesson", uselist=False)

    @staticmethod
    async def getContent(session: AsyncSession, lesson_id: int):
        query = select(Lesson).where(
            Lesson.id == lesson_id
        )

        tmp = await session.execute(query)

        lesson = tmp.scalar()
        lesson_table = mapping[lesson.type]
        result = await lesson_table.get_by_id(session, lesson_id)

        return result
