import unittest
import logging
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


class APITestCase(unittest.TestCase):

    def tearDown(self) -> None:
        logger.debug(self.tearDown.__name__)
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        logger.debug(cls.tearDownClass.__name__ + "\n")
        # os._exit(0)
        pass

    @classmethod
    def setUpClass(cls) -> None:
        logger.debug(cls.setUpClass.__name__)
        pass

    def setUp(self) -> None:
        logger.debug(self.setUp.__name__)
        pass

    def test_review_database_deletion(self):
        logger.debug(self.test_review_database_deletion.__name__)
        assert True

    def test_stuff_1(self):
        logger.debug(self.test_stuff_1.__name__)
        assert True

    def test_stuff_2(self):
        logger.debug(self.test_stuff_2.__name__)
        assert True


class AnotherTestCase(APITestCase):

    def test_another_testcase(self):
        logger.debug(self.test_another_testcase.__name__)
        assert True

    @classmethod
    def tearDownClass(cls) -> None:
        logger.debug(cls.tearDownClass.__name__ + "\n")
        os._exit(0)
