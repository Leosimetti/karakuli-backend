import datetime
import os
import shutil
import time

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

PROPER_USER = dict(
    email="user@example.com",
    username="sass",
    password="String1337"
)
PROPER_USER2 = dict(
    email="toltallydifferentuser@differentxample.com",
    username="anotherSass",
    password="String228"
)


class FakeRedis:
    content = {}

    async def get(self, key):
        try:
            res = self.content[key]
        except KeyError:
            res = None

        return res

    async def set(self, key, val):
        self.content[key] = val


# Todo @todo Find out what causes "RuntimeError: Event loop is closed"
@pytest.fixture
async def ac():
    from app import db_engine
    async with db_engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Faking redis
    from app.depends import get_redis
    FakeRedis.content = {}  # Todo check if doing so is OK
    app_object.dependency_overrides[get_redis] = FakeRedis

    async with AsyncClient(app=app_object, base_url="http://test") as client:
        await app.startup()
        yield client

    await app.shutdown()


DB_NAME = "test.sqlite"
DB_BACKUP = DB_NAME + ".back"


@pytest.fixture(scope="session", autouse=True)
def clear_db():
    names = [DB_NAME, DB_BACKUP]

    for name in names:
        if os.path.exists(name):
            os.remove(name)


@pytest.fixture
async def fill_db():  # Todo @todo change this to actual functions instead of endpoints
    # Todo create a database on first use and then yield it

    if not os.path.exists(DB_BACKUP):
        async with AsyncClient(app=app_object, base_url="http://test") as ac:
            await ac.post(LESSONS_PATH + "/radicals" + "/parse")
            await ac.post(LESSONS_PATH + "/kanji" + "/parse")
        shutil.copy(DB_NAME, DB_BACKUP)
    else:
        shutil.copy(DB_BACKUP, DB_NAME)


async def register_user(usr_model, ac: AsyncClient):
    res = await ac.post(
        AUTH_PATH + "/register",
        data=usr_model
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


async def register_and_get_token(ac, main_user: bool = True):
    from testing.test_auth import TestJWT

    usr = PROPER_USER if main_user else PROPER_USER2

    res = await register_user(usr, ac)
    email = usr["email"]
    psw = usr["password"]
    assert res.status_code == 201, res.content
    res = await TestJWT.login(TestJWT, email, psw, ac)
    assert res.status_code == 200, res.content
    token = res.json()["access_token"]
    return token
