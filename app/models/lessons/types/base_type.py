from sqlalchemy import Column, Integer, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr


class BaseType:
    @declared_attr
    def id(self):
        return Column(Integer, ForeignKey("lessons.id"), primary_key=True)

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        query = select(cls).where(cls.id == int(id))
        result = await session.execute(query)

        return result.scalar()
