import os
import logging
from uvicorn.config import logger

# DB
DATABASE_URL = os.getenv("DB_HOST")
if DATABASE_URL is None:
    logger.warning("Cannot load DATABASE_URL. Use sqlite file.")
    DATABASE_URL = "sqlite+aiosqlite:///test.sqlite"

# Encryption
ENCRYPTED_OMEGA_ABOBA_SECRET = "NAAAAAAAAAAAAAAAAAAAAAAAAA"

# CORS
ORIGINS = ["*"]
HEADERS = ["*"]
METHODS = ["*"]
