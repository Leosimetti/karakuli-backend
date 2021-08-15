from enum import Enum as _Enum

from sqlalchemy import Column, Integer
from sqlalchemy import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Base, BaseModel
from app.models.lessons.types import Kanji, Radical, Word, Grammar


class LessonType(_Enum):
    radical = Radical
    kanji = Kanji
    word = Word
    grammar = Grammar


class Lesson(Base, BaseModel):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(LessonType), nullable=False)

    # item = relationship(BaseType, back_populates="lesson", uselist=False)

    @staticmethod
    async def get_content(session: AsyncSession, lesson_id: int):
        query = select(Lesson).where(
            Lesson.id == lesson_id
        )

        tmp = await session.execute(query)

        lesson = tmp.scalar()
        lesson_table = lesson.type.value
        result = await lesson_table.get_by_lesson_id(session, lesson_id)

        return result
