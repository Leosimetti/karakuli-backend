from httpx import AsyncClient
from testing.conftest import REVIEWS_PATH, pytestmark


class TestReview:

    async def test_review_add_get(self, ac, fill_db):
        res = await ac.post(REVIEWS_PATH,
                            json={
                                "lesson_id": 22008,
                                "note": "string"
                            },
                            headers={"Authorization": f"Bearer {token}"}
                            )

    # https://github.com/pytest-dev/pytest-mock
    # datetime.datetime.now()
