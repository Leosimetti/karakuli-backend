import uuid
from typing import Optional


from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, UUID4, validator

from db import db
from users import UserDB, fastapi_users


class BaseWord(BaseModel):
    id: Optional[UUID4] = None
    writing: str
    reading: str
    meaning: str
    user: UUID4

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class CreateWord(BaseModel):
    writing: str
    reading: str
    meaning: str


router = APIRouter(tags=["words"])
words = db["words"]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(word: CreateWord, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    word_db = BaseWord(**word.dict(), user=user.id)
    await words.insert_one(word_db.dict())
    return word_db

@router.get("/my")
async def list(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    results = []
    async for raw_post in words.find({"user": user.id}):
        results.append(BaseWord(**raw_post))
    return results