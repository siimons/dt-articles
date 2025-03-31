import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app.api.v1.articles.views import router as articles_router
from app.api.v1.tags.views import router as tags_router
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
