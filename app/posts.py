import uuid
from typing import Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, UUID4, validator

from db import db
from users import UserDB, fastapi_users


class BasePost(BaseModel):
  id: Optional[UUID4] = None
  title: Optional[str] = None
  user: Optional[UUID4] = None

  @validator("id", pre=True, always=True)
  def default_id(cls, v):
      return v or uuid.uuid4()


class PostCreate(BaseModel):
  title: str


class PostDB(PostCreate, BasePost):
  user: UUID4


router = APIRouter(tags=["posts"])
posts = db["posts"]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(post: PostCreate, user: UserDB = Depends(fastapi_users.current_user(active=True))):
  post_db = PostDB(**post.dict(), user=user.id)
  await posts.insert_one(post_db.dict())
  return post_db

@router.get("/")
async def list(user: UserDB = Depends(fastapi_users.current_user(active=True))):
  results = []
  async for raw_post in posts.find({"user": user.id}):
    results.append(PostDB(**raw_post))
  return results
