import pytest
import pytest_asyncio
from fastapi import FastAPI, status
from httpx import AsyncClient, ASGITransport

from app.api.v1.articles.views import articles_router
from app.api.v1.tags.views import tags_router
from app.core.dependencies.common import db, cache, lifespan


@pytest.fixture
def app() -> FastAPI:
    """Создаёт экземпляр FastAPI с подключёнными роутерами."""
    app = FastAPI(lifespan=lifespan)
    app.include_router(articles_router)
    app.include_router(tags_router)
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI):
    """Создаёт асинхронный HTTP-клиент для тестирования API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Очищает тестовую базу данных перед каждым тестом."""
    await db.connect()
    async with db.pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            tables = ["users", "articles", "tags", "article_tags", "comments"]
            for table in tables:
                await cursor.execute(f"TRUNCATE TABLE {table};")

            await cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    yield
    await db.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_cache():
    """Очищает кэш перед каждым тестом."""
    await cache.connect()
    await cache.clear_cache()

    yield
    await cache.close()


@pytest_asyncio.fixture
async def create_test_tag(client: AsyncClient):
    """Создаёт тестовый тег через API и возвращает его данные."""
    async def _create_tag(name: str):
        response = await client.post("/api/v1/tags", json={"name": name})
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    return _create_tag


@pytest_asyncio.fixture
async def create_test_article(client: AsyncClient):
    """Создаёт тестовую статью с указанными параметрами."""
    async def _create_article(title: str, content: str, tags: list[int] = None):
        article_data = {
            "title": title,
            "content": content,
            "tags": tags or []
        }
        response = await client.post("/api/v1/articles", json=article_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()
    return _create_article