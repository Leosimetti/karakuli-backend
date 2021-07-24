from typing import Optional

from pydantic import BaseModel

from app.models.review import ReviewType


class ReviewSubmit(BaseModel):
    incorrect_answers: Optional[int]
    review_type: ReviewType
