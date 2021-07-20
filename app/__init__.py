from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

import app.settings

app = FastAPI(
    title="Karakuli",
    description="Cool japanese language thing",
    version="0.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_methods=settings.METHODS,
    allow_headers=settings.HEADERS,
    allow_credentials=True,
)

# Create engine.
db_engine = create_async_engine(
    settings.DATABASE_URL,
    future=True
)


@app.on_event("startup")
async def startup():
    async with db_engine.begin() as conn:
        from app.models import Base
        async with db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    import app.routers


@app.on_event('shutdown')
async def shutdown() -> None:
    await db_engine.dispose()
