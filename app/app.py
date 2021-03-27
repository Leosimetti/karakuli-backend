from fastapi import FastAPI

from db import db
from users import router as users_router
from dictionary import router as words_router

app = FastAPI()
app.include_router(users_router)
app.include_router(words_router, prefix="/words")

@app.on_event("shutdown")
async def shutdown():
    db.close()
