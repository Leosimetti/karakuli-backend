from sqlalchemy import Column, Integer, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr


class BaseType:

    @declared_attr
    def id(self):
        return Column(Integer, ForeignKey("lessons.id"), primary_key=True)

    @classmethod
    async def create(cls, session: AsyncSession, pydantic_model):
        from app.models.lessons.lesson import Lesson, LessonType

        lesson = Lesson(type=LessonType(cls))
        session.add(lesson)
        await session.commit()
        await session.refresh(lesson)

        radical = cls(**pydantic_model.dict(), id=lesson.id)
        session.add(radical)
        await session.commit()

        return radical

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        query = select(cls).where(cls.id == int(id))
        result = await session.execute(query)

        return result.scalar()
