from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class BaseModel:
    id = None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int, *fields_to_load):
        query = select(cls).where(cls.id == int(id))

        if fields_to_load:
            for field in fields_to_load:
                query = query.options(selectinload(field))

        result = await session.execute(query)

        return result.scalar()


from app.models.review import Review
from app.models.user import User
from app.models.lessons import Lesson, Word, Kanji, Grammar, Radical
from app.models.study import StudyList, StudyItem
