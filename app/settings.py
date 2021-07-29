import os
import logging
from uvicorn.config import logger

# DB
DATABASE_URL = os.getenv("BEKA_DB")
# Todo add checks whether BEKA is unreachable..
if DATABASE_URL is None:
    logger.warning("Cannot load BEKA_DB, using heroku DB.")
    DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    logger.warning("Cannot load DATABASE_URL, using sqlite file.")
    DATABASE_URL = "sqlite+aiosqlite:///test.sqlite"
else:
    DATABASE_URL = "postgresql+asyncpg://" + DATABASE_URL.split("://")[1]

# Auth
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('JWT_EXPIRE')
if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    logger.warning('Cannot load JWT_EXPIRE, setting to default (30).')
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if SECRET_KEY is None:
    logger.warning('Cannot load JWT_SECRET_KEY, generating random.')
    SECRET_KEY = os.urandom(64).hex()

# CORS
ORIGINS = ["*"]
HEADERS = ["*"]
METHODS = ["*"]
