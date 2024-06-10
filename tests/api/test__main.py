from loguru import logger


def test__root(client):
    res = client.get("/")  # noqa: F821
    logger.info("Message:", res.json().get("message"))  # Print the message for debugging purposes
    assert res.json().get("message") == "ok"
    assert res.status_code == 200

