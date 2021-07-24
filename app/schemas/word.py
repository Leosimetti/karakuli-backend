from pydantic import BaseModel
from typing import Optional


class WordInList(BaseModel):
    word_id: int
    list_id: int
    note: Optional[str]
    position: Optional[int]
