# Bounty Hunting API (Django + DRF + PostgreSQL)

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configuration: copy the example and edit your PostgreSQL credentials
cp .env.example .env
createdb bounty

python manage.py migrate
python manage.py seed_data      # 6 criminals + 12 hunt logs (safe to re-run: resets ids to 1)
python manage.py runserver
```


## Endpoints
| Method | URL | Notes |
|---|---|---|
| GET | /api/criminals/ | `min_reward`, `max_reward`, `armed`, `has_crew`, `escape_master`, `sort=reward\|-reward` (all combinable) |
| GET | /api/criminals/{id}/ | includes nested `hunts` |
| GET | /api/hunts/ | `?criminal_id=` |
| GET | /api/hunts/{id}/ | |
| POST | /api/hunts/ | `{criminal_id, success, notes}`; `created_at` is server-generated |
| PATCH | /api/hunts/{id}/ | only `success` / `notes`; `criminal_id` cannot change |
| DELETE | /api/hunts/{id}/ | 204 |

Status codes: 200, 201, 204, 400 (bad body/filter), 404 (unknown id), 405 (PUT not allowed).

## Postman
Import `bounty_hunting.postman_collection.json`, run `seed_data` first, then run the collection.
