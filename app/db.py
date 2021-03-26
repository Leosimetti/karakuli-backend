import os

import motor.motor_asyncio

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")


client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["database"]
