import os

import pytest

from app import create_app, db


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "test.db"
    uri = f"sqlite+pysqlite:///{database_path}"

    previous = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = uri

    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=uri,
    )

    with app.app_context():
        from app import models  # noqa: F401

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        if previous is not None:
            os.environ["DATABASE_URL"] = previous
        else:
            os.environ.pop("DATABASE_URL", None)


@pytest.fixture
def client(app):
    return app.test_client()
