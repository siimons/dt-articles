import aiomysql
from app.core.config import settings
from typing import List, Optional

from app.core.logging import logger


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Создание пула соединений с БД MySQL"""
        try:
            logger.info("Подключение к базе данных...")
            logger.info(f"Подключение к базе данных: host={settings.MYSQL_HOST}, port={settings.MYSQL_PORT}, user={settings.MYSQL_USER}")
            self.pool = await aiomysql.create_pool(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                db=settings.MYSQL_DATABASE,
                autocommit=True,  # Для автокоммита транзакций
                maxsize=10
            )
            logger.success("Успешное подключение к базе данных.")
        except Exception as e:
            logger.error(f"Ошибка при подключении к базе данных: {e}")
            raise

    async def close(self):
        """Закрытие соединений с БД"""
        try:
            if self.pool:
                logger.info("Закрытие соединений с базой данных...")
                self.pool.close()
                await self.pool.wait_closed()
                logger.success("Соединения с базой данных закрыты.")
        except Exception as e:
            logger.error(f"Ошибка при закрытии соединений с базой данных: {e}")

    async def fetch(self, query: str, *args) -> List[dict]:
        """Выполнение запроса, возвращающего результаты (например SELECT)"""
        try:
            logger.info(f"Выполнение запроса: {query} | Аргументы: {args}")
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    result = await cursor.fetchall()
                    logger.info(f"Запрос выполнен успешно. Получено строк: {len(result)}")
                    return result
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")
            raise

    async def execute(self, query: str, *args) -> Optional[int]:
        """Выполнение запроса без возвращаемых результатов (например INSERT, UPDATE, DELETE)"""
        try:
            logger.info(f"Выполнение запроса: {query} | Аргументы: {args}")
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(query, args)
                    lastrowid = cursor.lastrowid
                    logger.info(f"Запрос выполнен успешно. ID последней вставленной записи: {lastrowid}")
                    return lastrowid
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")
            raise


# Точка входа для запуска файла напрямую
if __name__ == "__main__":
    import asyncio

    async def test_database_connection():
        db = Database()
        try:
            await db.connect()
            logger.info("Тест подключения к базе данных выполнен успешно.")
        except Exception as e:
            logger.error(f"Тест подключения к базе данных завершился ошибкой: {e}")
        finally:
            await db.close()

    asyncio.run(test_database_connection())
