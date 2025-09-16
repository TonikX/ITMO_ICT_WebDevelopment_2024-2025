# Архитектура проекта с Celery и FastAPI

Проект состоит из нескольких сервисов, управляемых через Docker Compose:

## Сервисы

- **db** – PostgreSQL база данных.
- **redis** – брокер сообщений для Celery.
- **parser** – сервис для парсинга HTML страниц.
- **api** – основной FastAPI-приложение.
- **celery_worker** – воркер Celery для асинхронной обработки задач.

---

## Celery задачи

### 1. `celery_app`

- Асинхронно парсит одну страницу.
- Использует `httpx.AsyncClient` для загрузки HTML.
- Отправляет HTML на сервис `parser` для извлечения данных.


---

## FastAPI роуты

### `POST /parse_urls_task`

- Параметр: `url`  
- Создаёт задачу Celery `parse_url_tasks`.
- Возвращает `task_id`.

---



## Особенности

- Асинхронность через `asyncio` и `httpx`.
- Celery использует Redis как брокер и backend.
- Парсер работает в отдельном сервисе, чтобы разгрузить основной API.

## Docker Compose:
```python
version: "3.9"

services:
  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: andrey2002
      POSTGRES_DB: personal_finance
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: redis
    restart: always
    ports:
      - "6379:6379"

  api:
    build: .
    container_name: fastapi_app
    restart: always
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:andrey2002@db:5432/personal_finance
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000"

  parser:
    build: .
    container_name: parser_service
    restart: always
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:andrey2002@db:5432/personal_finance
    volumes:
      - .:/app
    command: bash -c "uvicorn Asyncio_fastApi:app --host 0.0.0.0 --port 8100"
    ports:
      - "8100:8100"


  celery_worker:
    build: .
    container_name: celery_worker
    restart: always
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    command: bash -c "celery -A app.celery_app worker --loglevel=info"

volumes:
  postgres_data:

```