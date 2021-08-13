from httpx import AsyncClient
from testing.conftest import LISTS_PATH, create_list, pytestmark

LIST_NAME = "coolList"


async def list_non_existent_testing(ac, token):
    for identifier in ["/10000", "/amogus2228", "/10/items", "/aboba/items"]:
        # Non-existent list
        res = await ac.get(LISTS_PATH + identifier)
        assert res.status_code == 404, res.content
        assert res.json() == {"detail": "List not found."}

        # Non-existent lesson
        res = await ac.post(LISTS_PATH + "/1" + "/items",
                            json={
                                "lesson_id": 22008,
                                "note": "string"
                            },
                            headers={"Authorization": f"Bearer {token}"}
                            )
        assert res.status_code == 404, res.content
        assert res.json() == {"detail": "Lesson not found."}

        # Non-existent list
        res = await ac.post(LISTS_PATH + "/1000" + "/items",
                            json={
                                "lesson_id": 1,
                                "note": "string"
                            },
                            headers={"Authorization": f"Bearer {token}"}
                            )
        assert res.status_code == 404, res.content
        assert res.json() == {"detail": "List not found."}


class TestList:
    current_id = 0

    async def test_creation(self, ac: AsyncClient, list_name=LIST_NAME, main_user: bool = True):

        # list creation
        self.current_id += 1
        user_id = 1 if main_user else 2

        expected_list = {
            "id": self.current_id,
            "user_id": user_id,
            "approved": False,
            "name": list_name,
            "description": None
        }

        token, res = await create_list(list_name, main_user, ac)
        assert res.status_code == 201, res.content
        assert res.json() == expected_list

        # Trying to get the list from a different endpoint
        for identifier in [self.current_id, list_name]:
            res = await ac.get(LISTS_PATH + f"/{identifier}")
            assert res.status_code == 200, res.content
            assert res.json() == expected_list

        # Creating a duplicate
        _, res = await create_list(list_name, main_user, ac)
        assert res.status_code == 409, res.content

        return token

    async def test_list_operations(self, ac, fill_db):

        # List initialization
        token1 = await self.test_creation(ac)
        list1_items_path_id = LISTS_PATH + "/1" + "/items"
        list1_items_path_name = LISTS_PATH + f"/{LIST_NAME}" + "/items"

        await list_non_existent_testing(ac, token1)

        # Adding items
        expected_item_ids = []
        for item_id, pos in zip([1, 30, 50], range(1, 4)):  # Todo mb dehardcode ids
            res = await ac.post(list1_items_path_id,
                                json={
                                    "lesson_id": item_id,
                                    "note": "string",
                                    "position": pos
                                },
                                headers={"Authorization": f"Bearer {token1}"}
                                )
            expected_item = {
                "lesson_id": item_id,
                "list_id": 1,
                "note": "string",
                "position": pos
            }
            expected_item_ids.append(item_id)
            assert res.status_code == 201, res.content
            assert res.json() == expected_item

            # Adding a duplicate
            res = await ac.post(list1_items_path_id,
                                json={
                                    "lesson_id": item_id,
                                    "note": "string"
                                },
                                headers={"Authorization": f"Bearer {token1}"}
                                )
            assert res.status_code == 409, res.content

        # Checking what was added via the list name and id
        for identifier in [list1_items_path_name, list1_items_path_id]:
            res = await ac.get(identifier)
            assert res.status_code == 200, res.content

            item_ids = list(map(lambda x: x["lesson_id"], res.json()))
            assert item_ids == expected_item_ids

        # Creating a second list
        list_2_name = "another_list"
        list_2_path_name = LISTS_PATH + f"/{list_2_name}" + "/items"
        token2 = await self.test_creation(ac, list_name=list_2_name, main_user=False)

        # Adding to the second list without specifying the position
        res = await ac.post(list_2_path_name,
                            json={
                                "lesson_id": 1,
                                "note": "string"
                            },
                            headers={"Authorization": f"Bearer {token2}"}
                            )
        assert res.status_code == 201, res.content

        # Using wrong tokens to add to lists
        for list_path, token in zip([list_2_path_name, list1_items_path_name], [token1, token2]):
            res = await ac.post(list_path,
                                json={
                                    "lesson_id": 1,
                                    "note": "string"
                                },
                                headers={"Authorization": f"Bearer {token}"}
                                )
            assert res.status_code == 403

    # Todo test item position/name/note updates

    # Todo test the /study endpoint
