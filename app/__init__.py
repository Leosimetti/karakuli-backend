import databases
import sqlalchemy

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.db import SQLAlchemyUserDatabase

import os

DATABASE_URL = os.getenv("DB_HOST", "sqlite:///./test.db")

app = FastAPI()


@app.on_event("startup")
async def startup():
    import app.endpoints


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
