from pydantic import BaseModel, Json
from typing import Optional


class WordInList(BaseModel):
    word_id: int
    note: Optional[str]
    position: Optional[int]


class WordCreate(BaseModel):
    meaning: str
    readings: str
    kanji: str
    example: str
    meta: Json
