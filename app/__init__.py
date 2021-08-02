from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
import aioredis

import app.settings

app = FastAPI(
    title="Karakuli",
    description="Cool japanese language thing",
    version="0.0.0",
    # openapi_url="/openapi.json",
    # root_path="/api/v1",
    docs_url="/"
)
app.router.prefix = "/api/v1"

# Todo stop the app if db is unreachable ???

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_methods=settings.METHODS,
    allow_headers=settings.HEADERS,
    allow_credentials=True,
)

db_engine = create_async_engine(
    settings.DATABASE_URL,
    future=True
)

redis = None


@app.on_event("startup")
async def startup():
    global redis  # Todo check if there is a better way to access the variable
    redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async with db_engine.begin() as conn:
        from app.models import Base
        # Todo fuck go back
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    import app.routers


@app.on_event('shutdown')
async def shutdown() -> None:
    await db_engine.dispose()
