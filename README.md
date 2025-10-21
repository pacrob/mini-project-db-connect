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

## Project layout

- `app/__init__.py` – Flask application factory and SQLAlchemy instance setup.
- `app/config.py` – Configuration values the app reads at startup.
- `app/models.py` – SQLAlchemy models defining the database tables (`Todo`, etc.).
- `wsgi.py` – Entry point for WSGI servers and the `flask run` command.
- `.env.example` – Sample environment variables for local development.
- `requirements.txt` – Python dependencies required by the project.
