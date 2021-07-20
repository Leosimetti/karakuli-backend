import os
import logging
from uvicorn.config import logger

# DB
DATABASE_URL = os.getenv("DB_HOST")
if DATABASE_URL is None:
    logger.warning("Cannot load DATABASE_URL. Use sqlite file.")
    DATABASE_URL = "sqlite+aiosqlite:///test.sqlite"

# Encryption
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if SECRET_KEY is None:
    logger.warning('Cannot load JWT_SECRET_KEY, generate random.')
    # Generate random, if not set.
    SECRET_KEY = os.urandom(64).hex()

# CORS
ORIGINS = ["*"]
HEADERS = ["*"]
METHODS = ["*"]
