from enum import Enum as _Enum

from sqlalchemy import Column, Integer, CheckConstraint
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, selectinload, backref

from app.models import Base, BaseModel
from app.models.lessons.types import Kanji, Radical, Word, Grammar


class LessonType(_Enum):
    radical = "rad"
    kanji = "kan"
    word = "wor"
    grammar = "grm"


def _generate_expression(a, b, c, d):
    a, b, c, d = list(map(lambda x: f"(NOT ({x} is NULL) )", [a, b, c, d]))
    # ~a~b~cd + ~a~bc~d + ~ab~c~d + a~b~c~d

    part_1 = f"((NOT {a}) AND (NOT {b}) AND (NOT {c}) AND {d} )"
    part_2 = f"((NOT {a}) AND (NOT {b}) AND ( {c}) AND (NOT {d}) )"
    part_3 = f"((NOT {a}) AND ( {b}) AND (NOT {c}) AND (NOT {d}) )"
    part_4 = f"(( {a}) AND (NOT {b}) AND (NOT {c}) AND (NOT {d}) )"

    return f"{part_1} OR {part_2} OR {part_3} OR {part_4}"


class Lesson(Base, BaseModel):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(LessonType), nullable=False)

    radical_id = Column(Integer, ForeignKey(Radical.id), nullable=True)
    kanji_id = Column(Integer, ForeignKey(Kanji.id), nullable=True)
    grammar_id = Column(Integer, ForeignKey(Grammar.id), nullable=True)
    word_id = Column(Integer, ForeignKey(Word.id), nullable=True)

    radical = relationship(Radical, backref=backref("lessons", uselist=False))
    kanji = relationship(Kanji, backref=backref("lessons", uselist=False))
    grammar = relationship(Grammar, backref=backref("lessons", uselist=False))
    word = relationship(Word, backref=backref("lessons", uselist=False))

    __table_args__ = (
        CheckConstraint(_generate_expression("radical_id", "kanji_id", "grammar_id", "word_id")),
    )

    @staticmethod
    async def getContent(session: AsyncSession, lesson_id: int):
        query = select(Lesson).where(
            Lesson.id == lesson_id
        )

        for field in [Lesson.kanji, Lesson.radical, Lesson.word, Lesson.kanji]:
            query = query.options(selectinload(field))
        res = await session.execute(query)

        lesson = res.scalar()

        mapping = {
            LessonType.radical: lesson.radical,
            LessonType.kanji: lesson.kanji,
            LessonType.word: lesson.word,
            LessonType.grammar: lesson.grammar,
        }
        return mapping[lesson.type]
