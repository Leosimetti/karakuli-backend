from fastapi import APIRouter, status, Depends
from .users import UserDB, fastapi_users
from datetime import datetime
from .db import db

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", status_code=status.HTTP_201_CREATED)
async def get_reviews(user: UserDB = Depends(fastapi_users.current_user(active=True))):
    review_db = db["reviews"]
    dictionary_db = db["dictionary"]
    user_review_db = review_db[str(user.id)]

    review_count = await user_review_db.count_documents({"review_date": {"$lt": datetime.now()}})
    study_count = await dictionary_db.count_documents({"user": user.id})

    result = {
        "studyLeft": study_count,
        "reviewLeft": review_count
    }

    return result
