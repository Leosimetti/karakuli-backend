from fastapi import FastAPI

from .db import db
from .users import router as users_router
from fastapi.middleware.cors import CORSMiddleware
from .dictionary import router as words_router

app = FastAPI()
app.include_router(users_router)
app.include_router(words_router, prefix="/words")

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:27017",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown():
    db.close()
