Make sure there is a .env file in the todoapp folder(same level as Dockerfile), create it if it doesn't exist. .env file should contain DJANGO_SECRET_KEY variable.
```bash
DJANGO_SECRET_KEY='your_secret_key'
```

Then run these two commands in the terminal.
```bash
docker build -t django-todo .
```

```bash
docker run -d --name django-todo --env-file .env -p 8000:8000 django-todo
```
