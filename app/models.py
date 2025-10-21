from datetime import datetime, timezone

from . import db


def current_time() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class Todo(db.Model):
    """Simple to-do item stored in Postgres."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=current_time, nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True), default=current_time, onupdate=current_time, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Todo {self.id} {self.title!r}>"
