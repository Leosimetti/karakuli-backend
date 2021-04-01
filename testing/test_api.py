import pytest
import inspect
from functools import wraps
from fastapi.testclient import TestClient
from app.app import app
from testing.conftest import logger

client = TestClient(app)


def logs(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug(f"Called async {func.__name__}")
            return await func(*args, **kwargs)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"Called {func.__name__}")
            return func(*args, **kwargs)

    return wrapper


@pytest.mark.usefixtures("class_fixture")
class TestStuff:

    @logs
    def test_stuff(self, logs):
        assert True

    @pytest.mark.asyncio
    @logs
    async def test_async_stuff(self, logs):
        assert True


@pytest.mark.asyncio
@logs
async def test_async(logs) -> None:
    import asyncio
    await asyncio.sleep(1)
    assert True


@logs
def test_sync(logs):
    assert True

    # def test_review_database_deletion(self):
    #     logger.debug(self.test_review_database_deletion.__name__)
    #     assert True
    #
    # def test_stuff_1(self):
    #     logger.debug(self.test_stuff_1.__name__)
    #     assert True
    #
    # def test_stuff_2(self):
    #     logger.debug(self.test_stuff_2.__name__)
    #     assert True
