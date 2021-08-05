import pytest

import app
from app.routers.auth import api as auth_api
from app.routers.lists import api as lists_api
from app.routers.lessons import api as lessons_api
from httpx import AsyncClient

app_object = app.app
pytestmark = pytest.mark.asyncio

BASE_PATH = app_object.router.prefix
AUTH_PATH = BASE_PATH + auth_api.prefix
LISTS_PATH = BASE_PATH + lists_api.prefix
LESSONS_PATH = BASE_PATH + lessons_api.prefix


# Todo Find out what causes "RuntimeError: Event loop is closed"

@pytest.fixture
async def ac():
    from app import db_engine
    async with db_engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(app=app_object, base_url="http://test") as client:
        await app.startup()
        yield client
    await app.shutdown()


@pytest.fixture
async def fill_db():
    async with AsyncClient(app=app_object, base_url="http://test") as ac:
        await ac.post(LESSONS_PATH + "/radicals" + "/parse")
        await ac.post(LESSONS_PATH + "/kanji" + "/parse")
