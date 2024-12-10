import aiomysql
from app.core.config import settings
from typing import List, Optional


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Создание пула соединений с БД MySQL"""
        self.pool = await aiomysql.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME,
            autocommit=True,  # Для автокоммита транзакций
            maxsize=10
        )

    async def close(self):
        """Закрытие соединений с БД"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def fetch(self, query: str, *args) -> List[dict]:
        """Выполнение запроса, возвращающего результаты (например SELECT)"""
        async with self.pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchall()
                return result

    async def execute(self, query: str, *args) -> Optional[int]:
        """Выполнение запроса без возвращаемых результатов (например INSERT, UPDATE, DELETE)"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, args)
                return cursor.lastrowid  # Возвращаем ID последней вставленной записи
