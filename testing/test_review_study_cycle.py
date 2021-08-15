import datetime

from httpx import AsyncClient
from testing.conftest import REVIEWS_PATH, pytestmark, register_and_get_token, LESSONS_PATH


class TestReview:

    async def test_review_add_get(self, ac, fill_db):

        # Creating users first
        token = await register_and_get_token(ac)
        token2 = await register_and_get_token(ac, main_user=False)

        # Not providing ant lessons for review
        for param in [{"lesson_id": []}, None]:
            res = await ac.post(REVIEWS_PATH,
                                headers={"Authorization": f"Bearer {token}"},
                                params=param
                                )
            assert res.status_code == 422, res.content

        # Actually adding reviews
        bad = [1488888, 8888888, 99999]
        real = [1, 4, 8, 7]
        res = await ac.post(REVIEWS_PATH,
                            headers={"Authorization": f"Bearer {token}"},
                            params={"lesson_id": bad + real}
                            )
        assert res.status_code == 201, res.content
        resulting_reviews = res.json()

        # Getting each review separately and combining them
        added = []
        for review_id in real:
            res = await ac.get(REVIEWS_PATH + f"/{review_id}",
                               headers={"Authorization": f"Bearer {token}"},
                               )
            assert res.status_code == 200, res.content
            for item in res.json():
                added.append(item)

            # Trying to access the file using as a different user
            # res = await ac.get(REVIEWS_PATH + f"/{review_id}",
            #                    headers={"Authorization": f"Bearer {token2}"},
            #                    )
            # assert res.status_code == 403, res.content

        # Trying to get a non-existent item
        res = await ac.get(REVIEWS_PATH + "/50000",
                           headers={"Authorization": f"Bearer {token}"},
                           )
        assert res.status_code == 404

        func = lambda x: x.get("lesson_id")
        assert sorted(resulting_reviews["added"], key=func) == sorted(added, key=func)
        assert resulting_reviews["already_added"] == []
        assert sorted(resulting_reviews["non_existent"]) == sorted(bad)

        # Adding duplicates
        res = await ac.post(REVIEWS_PATH,
                            headers={"Authorization": f"Bearer {token}"},
                            params={"lesson_id": bad + real}
                            )
        assert res.status_code == 201, res.content
        resulting_reviews = res.json()
        assert resulting_reviews["added"] == []
        assert sorted(resulting_reviews["already_added"], key=func) == sorted(added, key=func)
        assert sorted(resulting_reviews["non_existent"]) == sorted(bad)

    async def test_getting_due_reviews(self, ac, mocker, fill_db):

        # Creating a user first
        token = await register_and_get_token(ac)

        # Creating reviews for the user
        to_add = [1, 4, 8, 7]
        res = await ac.post(REVIEWS_PATH,
                            headers={"Authorization": f"Bearer {token}"},
                            params={"lesson_id": to_add}
                            )
        assert res.status_code == 201, res.content
        assert res.json()["added"] != []
        assert res.json()["already_added"] == []
        assert res.json()["non_existent"] == []

        # Getting corresponding lessons
        expected_lessons = []
        for lesson_id in to_add:
            res = await ac.get(LESSONS_PATH + f"/{lesson_id}")
            assert res.status_code == 200
            expected_lessons.append(res.json())

        # Getting not yet ready reviews
        res = await ac.get(REVIEWS_PATH,
                           headers={"Authorization": f"Bearer {token}"},
                           )
        assert res.status_code == 200, res.content
        assert res.json() == []

        # Advancing time and getting ready reviews
        class FakeDatetime:
            interval = datetime.timedelta(minutes=21)

            def __init__(self, interval):
                self.interval = interval

            def now(self=datetime.datetime):
                return datetime.datetime.now() + self.interval

        mocker.patch("app.routers.review.datetime", FakeDatetime)
        res = await ac.get(REVIEWS_PATH,
                           headers={"Authorization": f"Bearer {token}"},
                           )
        assert res.status_code == 200, res.content
        func = lambda x: x.get("lesson_id")
        assert sorted(res.json(), key=func) == sorted(expected_lessons, key=func)

        # Reviewing each lesson


        # Getting not yet ready reviews
        res = await ac.get(REVIEWS_PATH,
                           headers={"Authorization": f"Bearer {token}"},
                           )
        assert res.status_code == 200, res.content
        assert res.json() == []
