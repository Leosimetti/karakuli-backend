import uuid
from typing import Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, UUID4, validator

from scrapper import words

from db import db
from users import UserDB, fastapi_users


class BaseWord(BaseModel):
    id: Optional[UUID4] = None
    grade: str
    writing: str
    readings: str
    meaning: str
    strokes: int
    user: UUID4

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class CreateWord(BaseModel):
    grade: str
    writing: str
    readings: str
    meaning: str
    strokes: int


router = APIRouter(tags=["kanji"])
kanji_db = db["kanji"]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(word: CreateWord, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    word_db = BaseWord(**word.dict(), user=user.id)
    await kanji_db.insert_one(word_db.dict())
    return word_db


@router.post("/parse", status_code=status.HTTP_201_CREATED)
async def parse_wiki(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    for word in words():
        word_db = BaseWord(**word, user=user.id)
        await kanji_db.insert_one(word_db.dict())
    return "Done"


@router.get("/my")
async def list(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    results = []
    async for raw_post in kanji_db.find({"user": user.id}):
        results.append(BaseWord(**raw_post))
    return results
