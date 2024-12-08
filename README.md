# Article Service - Dev Talk

## Описание

dt-articles — это микросервис для работы со статьями в проекте **Dev Talk**. Он предоставляет RESTful API для создания, обновления, удаления и получения статей. Сервис разработан на базе FastAPI и использует MySQL в качестве базы данных. Взаимодействие с другими микросервисами происходит через Kafka.

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
│   │   │   ├── schemas.py
│   │   │   ├── views.py
│   │   │   ├── crud.py
│   │   │   └── services.py
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── cache_service.py
│   │   │   └── cache_exceptions.py
│   │   └── common/
│   │       ├── __init__.py
│   │       └── logging.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
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
│   ├── unit/
│   │   ├── test_articles.py
│   │   └── test_database.py
│   └── integration/
│       ├── test_endpoints.py
│       └── test_kafka.py
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

Нужно создать ручки с помощью FastAPI.

- POST `/api/articles` — создание новой статьи.
- PUT `/api/articles/{id}` — обновление существующей статьи по ID.
- DELETE `/api/articles/{id}` — удаление статьи по ID.
- GET `/api/articles` — получение списка всех ID статей.
- GET `/api/articles/{id}` — получение информации о статье по её ID.
