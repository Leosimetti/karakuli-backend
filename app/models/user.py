from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import BaseModel, Base
from app.models.study import StudyList
from app.models.review import Review


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(length=300), unique=True, nullable=False, index=True)
    username = Column(String(length=200), unique=True, nullable=False)
    password = Column(String(length=60), nullable=False)
    verified = Column(Boolean, default=False)
    current_list_id = Column(Integer, default=1)

    reviews = relationship(Review)
    created_study_lists = relationship(StudyList)

    # added_lessons = relationship("Lesson", back_populates="user")

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str):
        result = await session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar()
