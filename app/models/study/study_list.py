from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, Text,
                        except_)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.orderinglist import count_from_1, ordering_list
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, selectinload

from app.models import Base, BaseModel
from app.models.lessons import Lesson
from app.models.review import Review
from app.models.study.study_item import StudyItem


# Todo @todo dehardcode table references
class StudyList(Base, BaseModel):
    __tablename__ = "studylists"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    approved = Column(Boolean, default=False)

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text())
    img_url = Column(String, default="https://lh3.googleusercontent.com/proxy/TuyWP_h4w3SW2Satf3Q_9ay7i1xI9emvLKwd2D9up6-noNFknZKVek13cNsPNF6hhPYJ0c7sZNU2lOjhYYln3doPa9NyqkTLlyP1Zti0Trs35SQlPgDQ1qdN")

    user = relationship("User", back_populates="created_study_lists")
    items = relationship(
        StudyItem,
        order_by=StudyItem.position,
        collection_class=ordering_list("position", ordering_func=count_from_1),
    )

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
