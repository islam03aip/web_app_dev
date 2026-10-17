# Reading List

A small multi-container app: a Django REST API that reads and writes a reading
list stored in PostgreSQL.

## Run it

```bash
copy .env.example to .env, then edit .env: set a real DJANGO_SECRET_KEY and POSTGRES_PASSWORD
docker compose up --build
```

Web UI: http://localhost:8000/  
REST API: http://localhost:8000/api/  
(port configurable via `WEB_PORT`).

## Web pages

| URL | Description |
|-----|-------------|
| `/` | Library with status filter chips |
| `/books/add/` | Add a book |
| `/books/<id>/edit/` | Edit a book |
| `/books/<id>/delete/` | Delete confirmation |

## API endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/health/` | Checks the DB connection, returns book count |
| GET | `/api/books/` | List books (`?status=reading`, `?ordering=-rating`) |
| POST | `/api/books/` | Create a book |
| GET/PUT/PATCH/DELETE | `/api/books/<id>/` | Retrieve / update / delete |

`status` is one of `to_read`, `reading`, `finished`. `rating` is optional (1-5).
