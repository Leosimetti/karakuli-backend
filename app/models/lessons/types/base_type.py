import asyncpg.exceptions
from sqlalchemy import Column, ForeignKey, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr


class BaseType:
    @declared_attr
    def lesson_id(self):
        return Column(Integer, ForeignKey("lessons.id"), primary_key=True)

    @classmethod
    async def create(cls, session: AsyncSession, pydantic_model=None, dict=None):
        from app.models.lessons.lesson import Lesson, LessonType

        lesson = Lesson(type=LessonType(cls))
        session.add(lesson)
        await session.commit()
        await session.refresh(lesson)

        if pydantic_model:
            dict = pydantic_model.dict()

        # Todo @todo check if this try-except is retarded
        try:
            item = cls(**dict, lesson_id=lesson.id)
            session.add(item)
            await session.commit()
        except:
            await session.rollback()
            await session.delete(lesson)
            await session.commit()
            raise

        return item

    @classmethod
    async def get_by_lesson_id(cls, session: AsyncSession, lesson_id: int):
        query = select(cls).where(cls.lesson_id == int(lesson_id))
        result = await session.execute(query)

        return result.scalar()
