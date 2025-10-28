from app import db
from app.models import Todo


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


def test_index_page_renders_form(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Create a new task" in body
    assert "<form" in body


def test_patch_todo_updates_done_state(client):
    post_response = client.post("/todos", json={"title": "Finish tests"})
    todo_id = post_response.get_json()["id"]

    patch_response = client.patch(f"/todos/{todo_id}", json={"is_done": True})
    assert patch_response.status_code == 200
    assert patch_response.get_json()["is_done"] is True

    list_response = client.get("/todos")
    assert list_response.get_json()[0]["is_done"] is True


def test_delete_todo_removes_entry(client):
    post_response = client.post("/todos", json={"title": "Remove me"})
    todo_id = post_response.get_json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/todos")
    assert list_response.get_json() == []


def test_toggle_todo_via_form(client):
    create = client.post("/todos", json={"title": "HTML toggle"})
    todo_id = create.get_json()["id"]

    response = client.post(
        f"/todos/{todo_id}/toggle",
        data={"is_done": ["0","1"]},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Todo updated." in response.get_data(as_text=True)

    list_response = client.get("/todos")
    assert list_response.get_json()[0]["is_done"] is True

    response = client.post(
        f"/todos/{todo_id}/toggle",
        data={"is_done": ["0"]},
        follow_redirects=True,
    )

    assert response.status_code == 200

    list_response = client.get("/todos")
    assert list_response.get_json()[0]["is_done"] is False


def test_delete_todo_via_form(client):
    create = client.post("/todos", json={"title": "Delete via HTML"})
    todo_id = create.get_json()["id"]

    response = client.post(
        f"/todos/{todo_id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Todo deleted." in response.get_data(as_text=True)

    list_response = client.get("/todos")
    assert list_response.get_json() == []
