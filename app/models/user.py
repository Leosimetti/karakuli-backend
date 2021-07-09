from sqlalchemy import Column, Integer, String, Boolean
from app.models import BaseModel, Base


class User(Base, BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(length=300), unique=True, nullable=False, index=True)
    username = Column(String(length=200), unique=True, nullable=False)
    password = Column(String(length=60), nullable=False)
    verified = Column(Boolean, default=False)
