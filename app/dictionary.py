from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime
from scrapper import words

from .models import Review, ReviewSession, BaseWord, CreateWord
from .db import db
from .users import UserDB, fastapi_users
import pymongo

router = APIRouter(tags=["dictionary"])
dictionary_db = db["dictionary"]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_a_new_word(word: CreateWord, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    word_db = BaseWord(**word.dict(), user=user.id)
    await dictionary_db.insert_one(word_db.dict())
    return word_db


@router.post("/parse", status_code=status.HTTP_201_CREATED)
async def parse_wiki(user: UserDB = Depends(fastapi_users.current_user(verified=True))):
    for word in words():
        word_db = BaseWord(**word, user=user.id)
        await dictionary_db.insert_one(word_db.dict())
    return "Done"


@router.get("/study")
async def list_words_added_for_study(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    results = []
    async for raw_post in dictionary_db.find({"user": user.id}):
        results.append(BaseWord(**raw_post))
    return results


@router.post("/study", status_code=status.HTTP_201_CREATED,
             responses={
                 406: {"description": "The requested review already exists"},
                 404: {"description": "The requested word does not exists"}
             })
async def add_word_to_reviews(review_session: ReviewSession, user: UserDB = Depends(fastapi_users.current_user(active=True))):
    from .reviews import review_db
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
