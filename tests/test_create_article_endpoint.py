import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status

from app.api.v1.views import router
from app.core.database import Database

db = Database()


@pytest.fixture
def app() -> FastAPI:
    """
    Создаёт экземпляр приложения FastAPI с подключённым роутером.
    """
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        await db.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await db.close()

    app.include_router(router, prefix="/api/v1")
    return app


@pytest.mark.asyncio
async def test_create_article_success(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        payload = {
            "title": "How to set up a database connection",
            "content": "Who knows? I can't do it myself.",
            "tags": ["python", "mysql", "asyncio"]
        }
        response = await client.post("/api/v1/articles", json=payload)
        
        if response.status_code == status.HTTP_201_CREATED:
            response_data = response.json()
            assert response_data["title"] == payload["title"]
            assert response_data["content"] == payload["content"]
            assert set(response_data["tags"]) == set(payload["tags"])
        elif response.status_code == status.HTTP_409_CONFLICT:
            duplicate_response_data = response.json()
            assert duplicate_response_data["detail"] == f"Статья с заголовком '{payload['title']}' уже существует."
        else:
            assert False, f"Неожиданный статус-код: {response.status_code}"