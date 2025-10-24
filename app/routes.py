from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash

from . import db
from .models import Todo

bp = Blueprint("todos", __name__)


@bp.get("/")
def index():
    """Render the HTML interface showing existing todos and a create form."""
    todos = Todo.query.order_by(Todo.created_at.asc()).all()
    return render_template("todos/index.html", todos=todos)


@bp.get("/todos")
def list_todos():
    """Return all todo items ordered by creation time."""
    todos = Todo.query.order_by(Todo.created_at.asc()).all()
    return jsonify(
        [
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "is_done": todo.is_done,
                "created_at": todo.created_at.isoformat(),
                "updated_at": todo.updated_at.isoformat(),
            }
            for todo in todos
        ]
    )


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

        return (
            jsonify(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "is_done": todo.is_done,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat(),
                }
            ),
            201,
        )

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
