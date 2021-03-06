from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import selectinload

Base: DeclarativeMeta = declarative_base()


class BaseModel:
    id = None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int, *fields_to_load):
        # Todo @todo add boundary checking for ids (as some weird things happen for out of bound ids)
        query = select(cls).where(cls.id == int(id))

        if fields_to_load:
            for field in fields_to_load:
                query = query.options(selectinload(field))

        result = await session.execute(query)

        return result.scalar()


from app.models.lessons import Example, Lesson, Reading
from app.models.lessons.types import Grammar, Kanji, Radical, Word
from app.models.review import Review
from app.models.study import StudyItem, StudyList
from app.models.user import User
