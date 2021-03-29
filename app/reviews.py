from fastapi import APIRouter, Depends, status, HTTPException

import srs
from .db import db
from .users import UserDB, fastapi_users
from .models import Review, ReviewSession
from datetime import datetime

router = APIRouter(tags=["reviews"])
review_db = db["reviews"]


@router.get("/next-review", status_code=status.HTTP_201_CREATED)
async def get_next(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    user_db = review_db[str(user.id)]

    next_review = await user_db.find_one(sort=[("review_date", 1)])
    print(next_review)
    return Review.from_mongo(next_review)


# TODO make it work
@router.get("/due-reviews", status_code=status.HTTP_201_CREATED)
async def get_next(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    user_db = review_db[str(user.id)]

    next_review = await user_db.find({max: {"$review_date": datetime.now()}}, sort=[("review_date", 1)])
    print(next_review)

    return [Review.from_mongo(x) for x in next_review]


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
