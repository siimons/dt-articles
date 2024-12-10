import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status

from app.api.v1.views import router
from app.api.v1.schemas import ArticleCreate

@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return app

@pytest.mark.asyncio
async def test_create_article_success(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        payload = {
            "title": "Test Article",
            "content": "This is a test article content.",
            "tags": ["test", "article"]
        }
        response = await client.post("/api/v1/articles", json=payload)
        
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["title"] == payload["title"]
        assert response_data["content"] == payload["content"]
        assert set(response_data["tags"]) == set(payload["tags"])
