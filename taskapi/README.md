# Task Manager

A containerized task

## Architecture

| Service   | Image / Build               | Purpose                              | Exposed          |
|-----------|-----------------------------|--------------------------------------|------------------|
| `backend` | `backend/Dockerfile` | Django, DRF, Gunicorn, WhiteNoise    | `localhost:8000` |
| `db`      | `postgres:16-alpine`        | PostgreSQL database                  | internal only    |

- **Networking:** both services join the user-defined bridge network `app-network`. The backend reaches PostgreSQL through the service name `db` (`DB_HOST=db`) using Docker's built-in DNS. The database port is not published to the host.
- **Persistence:** PostgreSQL data lives in the named volume `taskapi_pgdata`, mounted at `/var/lib/postgresql/data`. Data survives `docker compose down` and container re-creation.
- **Startup order:** the backend starts only after the database healthcheck (`pg_isready`) passes. The entrypoint also waits for a successful connection, runs migrations, then starts Gunicorn.
- **Static files:** CSS is collected at image build time and served by WhiteNoise, so no separate web server is needed.
- **Configuration:** all settings come from environment variables loaded from `.env`.


## Quick start

Prerequisites: Docker and Docker Compose v2.
Make sure .env is configured.
```bash
docker compose up --build
```

Open:

| URL                              | Description                        |
|----------------------------------|------------------------------------|
| http://localhost:8000/           | Web interface (task list)          |
| http://localhost:8000/api/tasks/ | REST API (browsable in a browser)  |
| http://localhost:8000/health/    | Health check                       |

Stop the stack (data is kept):

```bash
docker compose down
```

Stop and delete all data:

```bash
docker compose down -v
```


## REST API documentation

Base URL: `http://localhost:8000`

Requests and responses use JSON. Send `Content-Type: application/json` on requests with a body. URLs must end with a trailing slash.

### Task object

| Field         | Type    | Notes                                               |
|---------------|---------|-----------------------------------------------------|
| `id`          | integer | Read-only, auto-generated                           |
| `title`       | string  | Required, up to 255 characters                      |
| `description` | string  | Optional, defaults to `""`                          |
| `status`      | string  | `pending` (default), `in_progress` or `done`        |
| `created_at`  | string  | Read-only, ISO 8601 timestamp                       |
| `updated_at`  | string  | Read-only, ISO 8601 timestamp                       |

### Endpoints

| Method | Path                | Description                   | Success |
|--------|---------------------|-------------------------------|---------|
| GET    | `/health/`          | Service and database health   | `200`   |
| GET    | `/api/tasks/`       | List tasks                    | `200`   |
| GET    | `/api/tasks/{id}/`  | Get a task by ID              | `200`   |
| POST   | `/api/tasks/`       | Create a task                 | `201`   |
| PUT    | `/api/tasks/{id}/`  | Update a task (full)          | `200`   |
| PATCH  | `/api/tasks/{id}/`  | Update a task (partial)       | `200`   |
| DELETE | `/api/tasks/{id}/`  | Delete a task                 | `204`   |

---

### GET /health/

**200 OK**
```json
{ "status": "ok", "database": "connected" }
```

**503 Service Unavailable**
```json
{ "status": "error", "database": "unavailable" }
```

---

### GET /api/tasks/

Returns all tasks ordered by `id`.

| Query parameter | Required | Description                                       |
|-----------------|----------|---------------------------------------------------|
| `status`        | No       | Filter by `pending`, `in_progress` or `done`      |

```bash
curl http://localhost:8000/api/tasks/
curl "http://localhost:8000/api/tasks/?status=done"
```

**200 OK**
```json
[
  {
    "id": 1,
    "title": "Write documentation",
    "description": "Document all endpoints",
    "status": "pending",
    "created_at": "2026-01-01T10:00:00.000000Z",
    "updated_at": "2026-01-01T10:00:00.000000Z"
  }
]
```

---

### GET /api/tasks/{id}/

```bash
curl http://localhost:8000/api/tasks/1/
```

**200 OK** returns a single task object.

**404 Not Found**
```json
{ "detail": "No Task matches the given query." }
```

---

### POST /api/tasks/

| Field         | Required | Type   |
|---------------|----------|--------|
| `title`       | Yes      | string |
| `description` | No       | string |
| `status`      | No       | string |

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Write documentation","description":"Document all endpoints"}'
```

**201 Created** returns the created task.

**400 Bad Request**
```json
{ "title": ["This field is required."] }
```

---

### PUT /api/tasks/{id}/

Full update. `title` is required.

```bash
curl -X PUT http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Write documentation","description":"Done","status":"done"}'
```

**200 OK** returns the updated task.

**400 Bad Request** for invalid data, **404 Not Found** if the task does not exist.

---

### PATCH /api/tasks/{id}/

Partial update. Send only the fields to change.

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

**200 OK** returns the updated task.

---

### DELETE /api/tasks/{id}/

```bash
curl -X DELETE http://localhost:8000/api/tasks/1/
```

**204 No Content** on success, **404 Not Found** if the task does not exist.

---

### Error responses

| Status | Meaning                          | Body example                                   |
|--------|----------------------------------|------------------------------------------------|
| 400    | Validation error                 | `{ "title": ["This field is required."] }`     |
| 404    | Task not found                   | `{ "detail": "No Task matches the given query." }` |
| 500    | Unexpected server error          | HTML or generic error response                 |

Invalid `status` values on create or update return `400` with a message listing the allowed choices. An unknown `status` filter on the list endpoint is ignored.