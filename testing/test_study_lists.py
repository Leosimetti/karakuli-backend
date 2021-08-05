from httpx import AsyncClient
from testing.conftest import LISTS_PATH, pytestmark


async def create_list(name: str, main_user: bool, ac: AsyncClient):
    from testing.test_auth import TestJWT, register_user, PROPER_USER, PROPER_USER2
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
    return res


class TestList:
    async def test_creation(self, ac: AsyncClient):
        res = await create_list("coolList", True, ac)
        assert res.status_code == 201, res.content

        res = await create_list("coolList", True, ac)
        assert res.status_code == 409, res.content

    async def test_add_items(self, ac, fill_db):
        pass
        # Todo try creating a different user and adding items
