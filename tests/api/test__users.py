from loguru import logger

# tests/api/test_users.py

from app.schemas.users import UserRead

def test_create_user(client_sqlite):
    user_data = {"email": "test_user@example.com", "name": "Test User", "password": "testpassword123"}
    response = client_sqlite.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = UserRead(**response.json())
    assert new_user.email == user_data["email"]
    assert new_user.name == user_data["name"]

def test_get_users(client_sqlite):
    response = client_sqlite.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)

def test_get_user(client_sqlite):
    user_data = {"email": "test_user@example.com", "name": "Test User", "password": "testpassword123"}
    create_response = client_sqlite.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    response = client_sqlite.get(f"/users/{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == user_data["email"]
    assert user["name"] == user_data["name"]

def test_update_user(client_sqlite):
    user_data = {"email": "test_user@example.com", "name": "Test User", "password": "testpassword123"}
    create_response = client_sqlite.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    updated_data = {"email": "updated_user@example.com", "name": "Updated User", "password": "newpassword123"}
    response = client_sqlite.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["email"] == updated_data["email"]
    assert updated_user["name"] == updated_data["name"]

def test_delete_user(client_sqlite):
    user_data = {"email": "test_user@example.com", "name": "Test User", "password": "testpassword123"}
    create_response = client_sqlite.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    response = client_sqlite.delete(f"/users/{user_id}")
    assert response.status_code == 204
    get_response = client_sqlite.get(f"/users/{user_id}")
    assert get_response.status_code == 404