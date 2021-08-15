from pydantic import BaseModel, Json
from typing import Optional


class LessonInList(BaseModel):
    lesson_id: int
    note: Optional[str]
    position: Optional[int]


# Todo @todo change str to constr with proper validation
# Todo @todo add a ENUM of word types
class WordCreate(BaseModel):
    meaning: str
    type: str
    links: Json
