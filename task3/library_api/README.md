# Library API (Django + Django REST Framework + SQLite)

## Setup
```bash
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env         # then set your own SECRET_KEY
python manage.py migrate
python manage.py runserver          # http://127.0.0.1:8000/api/
python manage.py test               # optional: run the test suite
```

## Environment variables (`.env`)
| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | insecure dev key |
| `DEBUG` | `True` / `False` | `False` |
| `ALLOWED_HOSTS` | comma-separated hosts | empty |
| `DB_NAME` | SQLite file name | `db.sqlite3` |

`.env` is git-ignored; commit only `.env.example`.

## Data model
- **Author** 1 --- N **Book** (`Book.author`, one-to-many)
- **Book** 1 --- N **Review** (`Review.book`, one-to-many)
- **Book** N --- N **Category** (`Book.categories`, many-to-many)

## Status codes
`200 OK` · `201 Created` · `204 No Content` (delete) · `400 Bad Request` (validation, returns `{field: [errors]}`) · `404 Not Found`

## Endpoints
Base URL: `http://127.0.0.1:8000`. All bodies/responses are JSON.

### Authors
| Method | URL | Body | Response |
|---|---|---|---|
| GET | `/api/authors/` | – | 200, list of authors |
| POST | `/api/authors/` | `name` (req), `bio`, `birth_date` (YYYY-MM-DD, not in future) | 201, created author |
| GET | `/api/authors/{id}/` | – | 200 author (with `book_count`) / 404 |
| PUT | `/api/authors/{id}/` | all fields (`name` required) | 200 updated author |
| PATCH | `/api/authors/{id}/` | any subset of fields | 200 updated author |
| DELETE | `/api/authors/{id}/` | – | 204 (also deletes their books) |
| GET | `/api/authors/{id}/books/` | – | 200, list of that author's books |

### Books
| Method | URL | Body / Params | Response |
|---|---|---|---|
| GET | `/api/books/` | query: `author`, `category`, `search` (title contains) | 200, list of books |
| POST | `/api/books/` | `title`, `isbn` (13 digits, unique), `published_year` (≤ current year), `price` (> 0), `author` (id), `categories` (list of ids, optional) | 201, created book |
| GET | `/api/books/{id}/` | – | 200 book (with `author_name`, `average_rating`) / 404 |
| PUT | `/api/books/{id}/` | all book fields | 200 |
| PATCH | `/api/books/{id}/` | any subset | 200 |
| DELETE | `/api/books/{id}/` | – | 204 |
| GET | `/api/books/{id}/reviews/` | – | 200, reviews of the book |
| POST | `/api/books/{id}/reviews/` | `reviewer_name`, `rating` (1–5), `comment` (optional) | 201, created review |

### Reviews
| Method | URL | Body | Response |
|---|---|---|---|
| GET | `/api/reviews/{id}/` | – | 200 / 404 |
| PUT / PATCH | `/api/reviews/{id}/` | `reviewer_name`, `rating`, `comment` | 200 |
| DELETE | `/api/reviews/{id}/` | – | 204 |

### Categories
| Method | URL | Body | Response |
|---|---|---|---|
| GET | `/api/categories/` | – | 200 |
| POST | `/api/categories/` | `name` (unique) | 201 |
| GET | `/api/categories/{id}/` | – | 200 / 404 |
| PUT / PATCH | `/api/categories/{id}/` | `name` | 200 |
| DELETE | `/api/categories/{id}/` | – | 204 |

### Example error (400)
```json
{"isbn": ["ISBN must be exactly 13 digits."], "price": ["Price must be greater than 0."]}
```

## Postman
Import `Library_API.postman_collection.json`. Run the collection in order (Runner): POST requests save ids into
collection variables (`author_id`, `book_id`, ...) used by later requests; the last folder cleans up. Change `base_url` if needed.
