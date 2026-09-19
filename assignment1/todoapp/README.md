
```bash
docker build -t django-todo .
```

```bash
docker run -d --name django-todo --env-file .env -p 8000:8000 django-todo
```
