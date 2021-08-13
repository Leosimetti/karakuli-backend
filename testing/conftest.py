import pytest

import app
from app.routers.auth import api as auth_api
from app.routers.lists import api as lists_api
from app.routers.lessons import api as lessons_api
from app.routers.review import api as review_api
from httpx import AsyncClient

app_object = app.app
pytestmark = pytest.mark.asyncio

BASE_PATH = app_object.router.prefix
AUTH_PATH = BASE_PATH + auth_api.prefix
LISTS_PATH = BASE_PATH + lists_api.prefix
LESSONS_PATH = BASE_PATH + lessons_api.prefix
REVIEWS_PATH = BASE_PATH + review_api.prefix


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
async def fill_db():  # Todo change this to actual functions instead of endpoints
    async with AsyncClient(app=app_object, base_url="http://test") as ac:
        await ac.post(LESSONS_PATH + "/radicals" + "/parse")
        await ac.post(LESSONS_PATH + "/kanji" + "/parse")


async def register_user(usr_model, ac: AsyncClient):
    res = await ac.post(
        AUTH_PATH + "/register",
        json=usr_model
    )

    return res


async def get_current_user(access_token, ac: AsyncClient):
    res = await ac.get(
        AUTH_PATH + "/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    return res


async def create_list(name: str, main_user: bool, ac: AsyncClient):
    from testing.test_auth import TestJWT, PROPER_USER, PROPER_USER2
    if main_user:
        await register_user(PROPER_USER, ac)
        email = PROPER_USER["email"]
        psw = PROPER_USER["password"]
    else:
        await register_user(PROPER_USER2, ac)
        email = PROPER_USER2["email"]
        psw = PROPER_USER2["password"]
    res = await TestJWT.login(TestJWT, email, psw, ac)
    token = res.json()["access_token"]

    res = await ac.post(LISTS_PATH,
                        params={"name": name},
                        headers={"Authorization": f"Bearer {token}"}
                        )
    return token, res