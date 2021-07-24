from sqlalchemy import Column, Integer, Boolean, String, Text, and_, except_
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.orderinglist import ordering_list

from app.models import Base, Word, StudyItem, Review, BaseModel


class StudyList(Base, BaseModel):
    __tablename__ = 'studylists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    approved = Column(Boolean, default=False)

    name = Column(String(100), unique=True)
    description = Column(Text())

    user = relationship("User", back_populates="created_study_lists")
    items = relationship("StudyItem", order_by="StudyItem.position",
                         collection_class=ordering_list('position'))

    @staticmethod
    async def get_n_new_words(session: AsyncSession, list_id: int, user_id: int, n: int):
        # Todo find out why negatives crash
        select_items = select(StudyItem.word_id).where(StudyItem.list_id == list_id)
        select_reviews = select(Review.word_id).where(Review.user_id == user_id)
        sas = except_(select_items, select_reviews)

        # Todo make this not retarded
        tmp = await session.execute(sas)
        word_ids = tmp.scalars().all()

        select_new_words = select(Word).where(Word.id.in_(word_ids))
        join_to_position = select_new_words.join(StudyItem.position, StudyItem.word_id == Word.id)
        filter_excess = join_to_position.order_by(StudyItem.position).limit(n)

        result = await session.execute(filter_excess)

        return result.scalars().all()

    @staticmethod
    async def get_by_name(session: AsyncSession, name: str, *fields_to_load):
        query = select(StudyList).where(
            StudyList.name == name,
        )

        if fields_to_load:
            for field in fields_to_load:
                query = query.options(selectinload(field))

        result = await session.execute(query)
        return result.scalar()
