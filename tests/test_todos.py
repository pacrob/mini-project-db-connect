from app.models import Todo
from app import db


def test_list_todos_starts_empty(client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_todo_persists_and_returns_item(app, client):
    payload = {"title": "Read specs", "description": "Understand Flask testing"}

    post_response = client.post("/todos", json=payload)
    assert post_response.status_code == 201

    data = post_response.get_json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_done"] is False
    assert "created_at" in data
    assert "updated_at" in data

    # Verify the record exists in the database.
    with app.app_context():
        item = db.session.get(Todo, data["id"])
        assert item is not None
        assert item.title == payload["title"]

    list_response = client.get("/todos")
    assert list_response.status_code == 200

    todos = list_response.get_json()
    assert len(todos) == 1
    assert todos[0]["id"] == data["id"]


def test_create_todo_requires_non_empty_title(client):
    response = client.post("/todos", json={"title": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Title is required."}
