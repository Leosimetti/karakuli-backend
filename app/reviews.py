from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, validator, Field, BaseConfig
from datetime import datetime
import pymongo

import srs
from .db import db
from .users import UserDB, fastapi_users
from .dictionary import dictionary_db
from .models import MongoModel, OID

router = APIRouter(tags=["reviews"])
review_db = db["reviews"]


class Review(MongoModel):
    # _id: UUID4
    word_id: OID = Field()
    srs_stage: int
    total_correct: int
    total_incorrect: int
    review_date: datetime

    # @validator("_id", pre=True, always=True)
    # def default_id(cls, v):
    #     return v or uuid.uuid4()


class ReviewSession(MongoModel):
    word_id: OID = Field()
    incorrect_answers: int


@router.post("/study", status_code=status.HTTP_201_CREATED,
             responses={
                 406: {"description": "The requested review already exists"},
                 404: {"description": "The requested word does not exists"}
             })
async def create(review_session: ReviewSession, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    user_db = review_db[str(user.id)]
    word_id = review_session.dict()['word_id']

    word = await dictionary_db.find_one({"_id": word_id})

    if word is None:
        raise HTTPException(status_code=404, detail="The requested word does not exists")

    review = {
        "word_id": word_id,
        "srs_stage": 0,
        "total_correct": 1,
        "total_incorrect": review_session.dict()['incorrect_answers'],
        "review_date": datetime.now()
    }

    initial_review = Review(**review)

    try:
        await user_db.insert_one(initial_review.mongo())
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=406, detail="The requested review already exists")

    return Review.from_mongo(initial_review.dict())


@router.post("/next-review", status_code=status.HTTP_201_CREATED)
async def get_next(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    user_db = review_db[str(user.id)]

    next_review = await user_db.find_one(sort=[("review_date", 1)])
    print(next_review)
    return Review.from_mongo(next_review)


@router.post("/submit", status_code=status.HTTP_201_CREATED,
             responses={
                 404: {"description": "The requested review does not exist"},
                 500: {"description": "Something went wrong when processing the review"}
             })
async def submit(review_session: ReviewSession, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    user_db = review_db[str(user.id)]

    review = await user_db.find_one({"word_id": review_session.word_id})
    if review is None:
        raise HTTPException(status_code=404, detail="The requested review does not exist")
    print(review)

    mistakes = review_session.incorrect_answers
    new_stage, new_date = srs.incorrect_answer(review["srs_stage"], mistakes,
                                               False) if mistakes > 0 else srs.correct_answer(review["srs_stage"],
                                                                                              False)

    updated_review = await user_db.update_one(
        {"word_id": review_session.word_id},
        {
            "$set": {
                "review_date": new_date,
                "srs_stage": new_stage,
                "total_incorrect": review["total_incorrect"] + mistakes,
                "total_correct": review["total_correct"] + 1,
            }
        }
    )

    if updated_review:
        return updated_review.raw_result
    else:
        raise HTTPException(status_code=500, detail="Something went wrong 💩")
