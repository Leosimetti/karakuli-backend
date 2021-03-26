from fastapi import FastAPI

from db import db
from posts import router as posts_router
from users import router as users_router

app = FastAPI()
app.include_router(users_router)
app.include_router(posts_router, prefix="/posts")

@app.on_event("shutdown")
async def shutdown():
    db.close()
