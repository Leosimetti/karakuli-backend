import asynctest
import logging
import inspect
import sys
from fastapi.testclient import TestClient
from app.app import app
import os

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
client = TestClient(app)


def logs(func):
    if inspect.iscoroutinefunction(func):
        async def wrapper(*args, **kwargs):
            logger.debug(f"async {func.__name__}")
            return await func(*args, **kwargs)
    else:
        def wrapper(*args, **kwargs):
            logger.debug(f"{func.__name__}")
            return func(*args, **kwargs)

    return wrapper


class APITestCase(asynctest.TestCase):

    @logs
    async def tearDown(self) -> None:
        pass

    @logs
    async def test_async(self) -> None:
        import asyncio
        await asyncio.sleep(1)
        assert True

    @logs
    def test_sync(self):
        assert True

    @logs
    async def setUp(self) -> None:
        pass

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
