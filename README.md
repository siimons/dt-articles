# Article Service - Dev Talk

## Описание

**dt-articles** — это микросервис для работы со статьями в проекте **Dev Talk**. Он предоставляет RESTful API для создания, обновления, удаления и получения статей. Сервис разработан на базе FastAPI и использует MySQL в качестве базы данных. Взаимодействие с другими микросервисами происходит через Kafka.

## Файловая структура микросервиса

```
dev-talk-articles/
|
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── articles/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── views.py
│   │   │   │   ├── repositories.py
│   │   │   │   ├── services.py
│   │   │   │   └── schemas.py
│   │   │   └── tags/
│   │   │       ├── __init__.py
│   │   │       ├── views.py
│   │   │       ├── repositories.py
│   │   │       ├── services.py
│   │   │       └── schemas.py
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── redis.py
│   │   └── common/
│   │       ├── __init__.py
│   │       └── utils.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── logging.py
│   │   └── dependencies.py
│   └── events/
│       ├── __init__.py
│       ├── producer.py
│       └── consumer.py
|
├── migrations/
│   ├── __init__.py
│   └── models.sql
|
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_storage_database.py
│   │   └── test_storage_redis.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── articles/
│   │   │   │   ├── test_create_draft_endpoint.py
│   │   │   │   ├── test_update_draft_endpoint.py
│   │   │   │   ├── test_publish_article_endpoint.py
│   │   │   │   ├── test_archive_article_endpoint.py
│   │   │   │   ├── test_delete_article_endpoint.py
│   │   │   │   ├── test_get_articles_endpoint.py
│   │   │   │   └── test_get_current_user_articles_endpoint.py
│   │   │   └── tags/
│   │   │       ├── test_create_tag_endpoint.py
│   │   │       ├── test_delete_tag_endpoint.py
│   │   │       └── test_get_tags_endpoint.py
│   │   └── events/
│   │       ├── __init__.py
│   │       ├── test_producer.py
│   │       └── test_consumer.py
│   └── e2e/
│       ├── __init__.py
│       └── test_article_flow.py
|
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Функциональность

### CRUD

#### Создание и управление статьями

- POST `/api/v1/articles/drafts` — создание черновика статьи.
- PATCH `/api/v1/articles/drafts/{article_id}` — обновление черновика статьи.
- PATCH `/api/v1/articles/{article_id}` — изменение статуса статьи.
- DELETE `/api/v1/articles/{article_id}` — удаление статьи.

#### Получение информации о статьях

- GET `/api/v1/articles` — получение списка всех статей.

    Параметры запроса:

    * `status` — фильтр по статусу (`draft`, `published`, `archived`).
    * `tags` — фильтр по тегам (`tags=python,fastapi`).

- GET `/api/v1/articles/current` — получение списка статей текущего пользователя.

    Параметры запроса:

    * `status` — фильтр по статусу.
    * `tags` — фильтр по тегам.

#### Управление тегами

- POST `/api/v1/tags` — создание нового тега.
- DELETE `/api/v1/tags/{tag_id}` — удаление тега.
- GET `/api/v1/tags` — получение списка всех тегов.
