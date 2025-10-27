# mini-project-db-connect

A demo app designed to explain how to connect a Flask app to a database.

## Getting started

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the sample environment file and adjust values as needed:

   ```bash
   cp .env.example .env
   ```

   Update `DATABASE_URL` if your local Postgres credentials differ.
4. Ensure your Postgres instance has a database that matches `DATABASE_URL`.
   You can run the following to run Postgres in a Docker container:

   ```bash
   docker run --name todo-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=todo_app -p 5432:5432 -d postgres:16
   ```

   To enter the Postgres shell, run:

   ```bash
   docker exec -it todo-postgres psql -U postgres -d todo_app
   ```

5. Initialize the database tables:

   ```bash
   flask init-db
   ```

6. Start the development server:

   ```bash
   flask run
   ```

7. Hit `http://127.0.0.1:5000/healthz` to confirm the app is running with the configured settings.

## Using the API

With the server running you can interact with the todos endpoints:

- List todos:

  ```bash
  curl http://127.0.0.1:5000/todos
  ```

- Create a todo:

  ```bash
  curl -X POST http://127.0.0.1:5000/todos \
    -H "Content-Type: application/json" \
    -d '{"title": "Walk through the code", "description": "Explain the Flask and SQLAlchemy flow"}'
  ```

- Mark a todo done:

  ```bash
  curl -X PATCH http://127.0.0.1:5000/todos/1 \
    -H "Content-Type: application/json" \
    -d '{"is_done": true}'
  ```

- Delete a todo:

  ```bash
  curl -X DELETE http://127.0.0.1:5000/todos/1
  ```

## Web UI

Navigate to `http://127.0.0.1:5000/` to use the HTML interface. It includes a form to add new tasks, checkboxes to mark items complete (with strike-through styling), and delete buttons to remove entries.

## Running tests

Pytest is configured to spin up a temporary SQLite database and exercise the API using Flask's test client:

```bash
pytest
```

## Project layout

- `app/__init__.py` – Flask application factory and SQLAlchemy instance setup.
- `app/config.py` – Configuration values the app reads at startup.
- `app/models.py` – SQLAlchemy models defining the database tables (`Todo`, etc.).
- `app/routes.py` – Blueprint exposing JSON endpoints for listing and creating todos.
- `tests/` – Pytest suite with fixtures and endpoint coverage.
- `wsgi.py` – Entry point for WSGI servers and the `flask run` command.
- `.env.example` – Sample environment variables for local development.
- `requirements.txt` – Python dependencies required by the project.
