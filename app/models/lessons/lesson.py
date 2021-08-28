from enum import Enum as _Enum

from sqlalchemy import Column, Enum, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base, BaseModel
from app.models.lessons.types import Grammar, Kanji, Radical, Word


class LessonType(_Enum):
    radical = Radical
    kanji = Kanji
    word = Word
    grammar = Grammar


class Lesson(Base, BaseModel):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(LessonType), nullable=False)

    # item = relationship(BaseType, back_populates="lesson", uselist=False)

    @staticmethod
    async def get_content(session: AsyncSession, lesson_id: int):
        lesson = await Lesson.get_by_id(session, lesson_id)
        item_table = lesson.type.value
        result = await item_table.get_by_lesson_id(session, lesson_id)

        return result
