from pydantic import BaseModel, Json
from typing import Optional


class LessonInList(BaseModel):
    lesson_id: int
    note: Optional[str]
    position: Optional[int]


# Todo change str to constr with proper validation
# Todo add a ENUM of word types
class WordCreate(BaseModel):
    meaning: str
    type: str
    links: Json
