Make sure there is a .env file and that it contains DJANGO_SECRET_KEY variable.
```bash
DJANGO_SECRET_KEY='your_secret_key'
```

```bash
docker build -t django-todo .
```

```bash
docker run -d --name django-todo --env-file .env -p 8000:8000 django-todo
```
