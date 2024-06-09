from loguru import logger

from app.schemas.users import UserRead


def test_create_user(client):
    res = client.post(
        "/users/",
        json={"email": "hello123@gmail.com", "name": "pierrick", "password": "password123"},
    )
    new_user = UserRead(**res.json())
    logger.info(res.json())
    assert res.status_code == 201
    assert res.json().get("email") == "hello123@gmail.com"
