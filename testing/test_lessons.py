from httpx import AsyncClient
from testing.conftest import LESSONS_PATH, pytestmark


class TestKanji:
    PATH = LESSONS_PATH + "/kanji"

    # async def test_parse(self, ac: AsyncClient):
    #     res = await ac.post(self.PATH + "/parse")
    #     assert res.text == '"Done"'
    #
    #     res = await ac.post(self.PATH + "/parse")
    #     assert res.text == '"Already parsed"'

    async def test_add(self, ac: AsyncClient):
        assert False, "Not implemented"


# Todo @todo refactor using inheritance or delete
class TestRadicals:
    PATH = LESSONS_PATH + "/radicals"

    # async def test_parse(self, ac: AsyncClient):
    #     res = await ac.post(self.PATH + "/parse")
    #     assert res.text == '"Done"'
    #
    #     res = await ac.post(self.PATH + "/parse")
    #     assert res.text == '"Already parsed"'

    async def test_add(self, ac: AsyncClient):
        assert False, "Not implemented"
