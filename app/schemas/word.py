from pydantic import BaseModel
from typing import Optional


class WordList(BaseModel):
    word_id: int
    list_id: int
    note: Optional[str]
    position: Optional[int]
