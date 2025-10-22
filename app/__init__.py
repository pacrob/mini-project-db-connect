import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance created at module level so models can import it later.
db = SQLAlchemy()


def create_app(config_object: str = "app.config.Config") -> Flask:
    """Application factory that wires configuration and extensions."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    from .routes import bp as todos_bp

    app.register_blueprint(todos_bp)
    
    @app.cli.command("init-db")
    def init_db() -> None:
        """Initialize the database."""
        with app.app_context():
            from . import models  # noqa: F401

            db.create_all()
            db.session.remove()
            db.engine.dispose()
        click.echo("Database initialized.")

    @app.get("/healthz")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app
