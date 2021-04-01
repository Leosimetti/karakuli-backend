import pytest
import logging
import sys

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


@pytest.fixture(scope="session", autouse=True)
def session_fixture(request):
    logger.debug(f"Called {request.fixturename} before tests")

    def finish():
        logger.debug(f"Called {request.fixturename} after tests")

    request.addfinalizer(finish)


@pytest.fixture
def logs(request):
    test_class = request.cls.__name__ + "." if request.cls else ""
    logger.debug(f"Called {request.fixturename} before {test_class}{request.function.__name__}")
    yield
    logger.debug(f"Called {request.fixturename} after {test_class}{request.function.__name__}")


@pytest.fixture(scope="class")
def class_fixture(request):
    test_class = request.cls.__name__ + "." if request.cls else ""
    logger.debug(f"Called {request.fixturename} before {test_class}")
    yield
    logger.debug(f"Called {request.fixturename} after {test_class}")
