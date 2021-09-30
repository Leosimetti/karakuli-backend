from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

import app.settings as settings

app = FastAPI(
    title="Karakuli",
    description="Cool japanese language thing",
    version="0.0.0",
    docs_url="/",
)
app.router.prefix = "/api/v1"


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_methods=settings.METHODS,
    allow_headers=settings.HEADERS,
    allow_credentials=True,
)

# Todo @todo add health checks for the database?
db_engine = create_async_engine(settings.DATABASE_URL, future=True)

# Todo @todo PLZ DO NOT FORGET TO REMOVE THIS IN PROD OR YOU ARE RETARD
# import os
#
# if os.getenv("IS_DEV"):

@app.router.post("/drop")
async def drop_and_recreate_db():
    async with db_engine.begin() as conn:
        from app.models import Base

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return "DONE"


@app.on_event("startup")
async def startup():
    import app.routers


@app.on_event("shutdown")
async def shutdown() -> None:
    await db_engine.dispose()
