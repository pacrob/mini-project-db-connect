from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from . import db
from .models import Todo

bp = Blueprint("todos", __name__)


def serialize_todo(todo: Todo) -> dict:
    return {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "is_done": todo.is_done,
        "created_at": todo.created_at.isoformat(),
        "updated_at": todo.updated_at.isoformat(),
    }


@bp.get("/")
def index():
    """Render the HTML interface showing existing todos and a create form."""
    todos = Todo.query.order_by(Todo.created_at.asc()).all()
    return render_template("todos/index.html", todos=todos)


@bp.get("/todos")
def list_todos():
    """Return all todo items ordered by creation time."""
    todos = Todo.query.order_by(Todo.created_at.asc()).all()
    return jsonify([serialize_todo(todo) for todo in todos])


@bp.post("/todos")
def create_todo():
    """Create a new todo item from JSON payload."""
    if request.is_json:
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        description = (data.get("description") or "").strip() or None

        if not title:
            return jsonify({"error": "Title is required."}), 400

        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()

        return jsonify(serialize_todo(todo)), 201

    title = (request.form.get("title") or "").strip()
    description = (request.form.get("description") or "").strip() or None

    if not title:
        flash("Title is required to create a todo.", "error")
        return redirect(url_for("todos.index"))

    todo = Todo(title=title, description=description)
    db.session.add(todo)
    db.session.commit()
    flash("Todo created successfully.", "success")

    return redirect(url_for("todos.index"))


@bp.patch("/todos/<int:todo_id>")
def update_todo(todo_id: int):
    """Update a todo item via JSON payload."""
    if not request.is_json:
        abort(415)

    todo = db.session.get(Todo, todo_id)
    if todo is None:
        abort(404)

    data = request.get_json() or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "Title is required."}), 400
        todo.title = title
    if "description" in data:
        description = data.get("description")
        todo.description = description.strip() if isinstance(description, str) else None
    if "is_done" in data:
        value = data["is_done"]
        if isinstance(value, str):
            todo.is_done = value.lower() in {"1", "true", "yes", "on"}
        else:
            todo.is_done = bool(value)

    db.session.commit()
    return jsonify(serialize_todo(todo))


@bp.post("/todos/<int:todo_id>/toggle")
def toggle_todo(todo_id: int):
    """Toggle completion via HTML form submission."""
    todo = db.session.get(Todo, todo_id)
    if todo is None:
        abort(404)

    values = request.form.getlist("is_done")
    todo.is_done = any(value in {"1", "true", "on"} for value in values)

    db.session.commit()
    flash("Todo updated.", "success")
    return redirect(url_for("todos.index"))


@bp.delete("/todos/<int:todo_id>")
def delete_todo(todo_id: int):
    """Delete a todo entry from the database via JSON request."""
    todo = db.session.get(Todo, todo_id)
    if todo is None:
        abort(404)

    db.session.delete(todo)
    db.session.commit()
    return ("", 204)


@bp.post("/todos/<int:todo_id>/delete")
def delete_todo_html(todo_id: int):
    """Delete a todo entry via HTML form submission."""
    todo = db.session.get(Todo, todo_id)
    if todo is None:
        abort(404)

    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted.", "success")
    return redirect(url_for("todos.index"))
