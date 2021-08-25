import logging
import os

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

# Redis db
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL is None:
    logger.warning("Could not load redis URL. Problems with token refresh will occur.")

# Auth
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_EXPIRE")
if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    logger.warning("Cannot load JWT_EXPIRE, setting to default (30).")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_REFRESH")
if REFRESH_TOKEN_EXPIRE_MINUTES is None:
    logger.warning("Cannot load JWT_REFRESH, setting to default (Expire*2).")
    REFRESH_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES * 2

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if SECRET_KEY is None:
    logger.warning("Cannot load JWT_SECRET_KEY, generating random.")
    SECRET_KEY = os.urandom(64).hex()

# CORS
ORIGINS = ["*"]
HEADERS = ["*"]
METHODS = ["*"]
