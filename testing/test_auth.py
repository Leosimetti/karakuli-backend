from httpx import AsyncClient

from testing.conftest import AUTH_PATH, register_user, get_current_user, pytestmark

PROPER_USER = user = dict(
    email="user@example.com",
    username="sass",
    password="String1337"
)
PROPER_USER2 = dict(
    email="toltallydifferentuser@differentxample.com",
    username="anotherSass",
    password="String228"
)


class TestGeneral:
    async def test_create_user(self, ac: AsyncClient):
        res = await register_user(PROPER_USER, ac)

        # Removing the password because it should be hidden
        expected_result = {"id": 1, "verified": False, **PROPER_USER}
        expected_result.pop("password")

        assert res.status_code == 201, res.text
        assert res.json() == expected_result, res.json()

    async def test_create_user_duplicate(self, ac: AsyncClient):
        res = await register_user(PROPER_USER, ac)
        assert res.status_code == 201, res.text

        res = await register_user(PROPER_USER, ac)
        assert res.status_code == 409, res.text


class TestJWT:
    JWT_PATH = AUTH_PATH + "/jwt"

    async def login(self, email, password, ac: AsyncClient):
        res = await ac.post(
            self.JWT_PATH + "/login",
            data=dict(
                username=email,
                password=password
            )
        )

        return res

    async def test_login(self, ac: AsyncClient):
        # Registering
        res = await register_user(PROPER_USER, ac)
        assert res.status_code == 201, res.text

        # Logging in
        email = PROPER_USER["email"]
        psw = PROPER_USER["password"]
        res = await self.login(email, psw, ac)
        assert res.status_code == 200, res.content
        access_token = res.json()["access_token"]

        # Trying to use the received token
        res = await get_current_user(access_token, ac)
        assert res.status_code == 200, res.content

        # Removing the password because it gets hashed
        expected_user_data = dict(**PROPER_USER, verified=False, current_study_list=1, id=1)
        expected_user_data.pop("password")

        user_data = res.json()
        user_data.pop("password")

        assert user_data == user_data

    async def test_incorrect_credentials_login(self, ac: AsyncClient):
        res = await register_user(PROPER_USER, ac)
        assert res.status_code == 201, res.text

        email = PROPER_USER["email"]
        psw = PROPER_USER["password"]

        email2 = PROPER_USER2["email"]
        psw2 = PROPER_USER2["password"]

        # Wrong password
        res = await self.login(email, psw2, ac)
        assert res.status_code == 404, res.content
        assert res.json() == {"detail": "Incorrect password"}, res.json()

        # Non-existent email
        res = await self.login(email2, psw, ac)
        assert res.status_code == 404, res.content
        assert res.json() == {"detail": "Invalid Credentials"}, res.json()

        # Non-existent email and password
        res = await self.login(email2, psw2, ac)
        assert res.status_code == 404, res.content
        assert res.json() == {"detail": "Invalid Credentials"}, res.json()

    # Todo understand why not work
    async def test_token_refresh(self, ac: AsyncClient):
        async def refresh(tkn):
            return await ac.post(self.JWT_PATH + "/refresh",
                                 params={"refresh_token": tkn})

        # Register and login
        res = await register_user(PROPER_USER, ac)
        assert res.status_code == 201, res.text
        email = PROPER_USER["email"]
        psw = PROPER_USER["password"]

        res = await self.login(email, psw, ac)
        assert res.status_code == 200, res.content
        refresh_token = res.json()["refresh_token"]

        # Proper refresh
        res = await refresh(refresh_token)
        assert res.status_code == 200, res.content
        new_refresh_token = res.json()["refresh_token"]

        # Another proper refresh
        res = await refresh(new_refresh_token)
        assert res.status_code == 200, res.content

        # Using old tokens
        for token in [refresh_token, new_refresh_token]:
            res = await refresh(token)
            assert res.status_code == 401, res.content

        # Using a bogus token
        from random import shuffle
        refresh_token = str(shuffle(list(refresh_token)))
        res = await refresh(refresh_token)
        assert res.status_code == 401, res.content
