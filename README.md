## ML Service — Emotion Analysis

Service for text emotion analysis: FastAPI API, frontend with Jinja templates + nginx static, background ML workers and PostgreSQL. Everything is wired together via Docker Compose.

### Architecture

- **app**: FastAPI application, API + HTML pages (`/`, `/sign-in`, `/sign-up`).
- **ml_worker**: workers that read tasks from RabbitMQ and send predictions back to the API.
- **database**: PostgreSQL.
- **rabbitmq**: message broker + management UI at `http://localhost:15672`.
- **web-proxy**: nginx, serves static assets and proxies API to FastAPI.

### Prerequisites

- Docker and Docker Compose.
- Host port `80` is free (used by nginx).

### Configuration

There are example configuration files already in the repo:

- `app/.env` — DB settings, JWT, and ML task price (example below):

```env
DB_HOST=database
DB_PORT=5432
DB_USER=test_user
DB_PASS=test_pw
DB_NAME=test_db
APP_NAME="Emotion Recognition Service for Neurodiverse Communication"
APP_DESCRIPTION="API for ml service"
DEBUG=False
API_VERSION=1.0
AUTH_SECRET_KEY=test_key
AUTH_COOKIE_NAME=access_token
RUN_TASK_PRICE=0.1
RMQ_HOST=rabbitmq
RMQ_PORT=5672
RMQ_USER=test_user
RMQ_PASS=test_pw
RMQ_QUEUE=ml_task_queue
S2S_SECRET_KEY=test_s2s_key
```

- `ml_worker/.env` — similar file for the worker (must contain at least `RMQ_*`, `APP_URL`, `S2S_SECRET_KEY`). Make sure values stay in sync with `app/.env`.

Adjust these files before running if needed.

### Quick start

From the project root:

```bash
docker compose up --build
```

Compose will start:

- `ml-service-api` — FastAPI app (`app/api.py`).
- `ml-service-work` — ML workers (2 replicas).
- `ml-service-nginx` — frontend + reverse proxy.
- `ml-service-db` — PostgreSQL.
- `ml-service-rabbitmq` — RabbitMQ.

Once containers are `healthy`:

- Open the web UI: `http://localhost/`
  - Dashboard: `http://localhost/`
  - Sign in: `http://localhost/sign-in`
  - Sign up: `http://localhost/sign-up`
- RabbitMQ Management UI: `http://localhost:15672` (credentials from `RABBITMQ_USER` / `RABBITMQ_PASS`).

### Running tests

API tests run inside the app container using `pytest` and a separate SQLite DB `testing.db`.

Run all tests:

```bash
docker exec -w /app ml-service-api python -m pytest tests -vv
```

Run a specific test file:

```bash
docker exec -w /app ml-service-api python -m pytest tests/test_sign_up.py -vv
```

### Notes

- Static frontend assets live in `nginx/static`, HTML templates — in `app/view`.
- All frontend HTTP calls to the API go through nginx to the same host/port (`/api/...`).
- Auth is based on JWT stored in an httpOnly cookie (`AUTH_COOKIE_NAME` from `.env`).

