from typing import Optional

from app.api.v1.tags.repositories import TagRepository
from app.api.storage.redis import RedisManager

from app.api.v1.tags.schemas import (
    TagCreate,
    Tag,
    TagList,
)

from app.api.v1.exceptions import (
    TagAlreadyExistsException,
    TagNotFoundException,
    TagInUseException,
    TagDeletionException,
    TagValidationException,
)

from app.core.settings import settings
from app.core.logging import logger


class TagService:
    """Сервис для управления тегами с кэшированием."""

    def __init__(self, tag_repo: TagRepository, cache: RedisManager):
        self.tag_repo = tag_repo
        self.cache = cache
        self.cache_prefix = "tag:"
        self.cache_ttl = 3600  # 1 час

    async def _get_cache_key(self, key: str) -> str:
        """Генерирует ключ для кэша."""
        return f"{self.cache_prefix}{key}"

    async def _invalidate_tag_cache(self, tag_id: int, tag_name: str) -> None:
        """Инвалидирует кэш для тега."""
        await self.cache.delete(await self._get_cache_key(f"id:{tag_id}"))
        await self.cache.delete(await self._get_cache_key(f"name:{tag_name}"))
        await self.cache.delete_pattern(await self._get_cache_key("list:*"))

    async def create_tag(self, tag_data: TagCreate) -> Tag:
        """Создать новый тег."""
        try:
            # Проверка существования тега
            existing_tag = await self.tag_repo.get_tag_by_name(tag_data.name)
            if existing_tag:
                raise TagAlreadyExistsException(tag_data.name)

            # Создание тега
            tag_id = await self.tag_repo.create_tag(tag_data.name)
            if not tag_id:
                raise TagValidationException("Не удалось создать тег")

            # Получаем полные данные тега
            tag = await self.tag_repo.get_tag_by_id(tag_id)
            if not tag:
                raise TagNotFoundException(tag_id)

            logger.info(f"Создан новый тег: {tag['name']} (ID: {tag_id})")
            return Tag(**tag)

        except ValueError as e:
            logger.error(f"Ошибка валидации тега: {str(e)}")
            raise TagValidationException(str(e))
        except Exception as e:
            logger.error(f"Ошибка при создании тега: {str(e)}")
            raise TagValidationException("Ошибка при создании тега")

    async def delete_tag(self, tag_id: int) -> None:
        """Удалить тег."""
        try:
            # Проверка существования тега
            tag = await self.tag_repo.get_tag_by_id(tag_id)
            if not tag:
                raise TagNotFoundException(tag_id)

            # Проверка использования тега
            if await self.tag_repo.is_tag_used(tag_id):
                raise TagInUseException(tag_id)

            # Удаление тега
            deleted = await self.tag_repo.delete_tag(tag_id)
            if not deleted:
                raise TagDeletionException(tag_id)

            # Инвалидация кэша
            await self._invalidate_tag_cache(tag_id, tag["name"])
            logger.info(f"Тег удалён: {tag['name']} (ID: {tag_id})")

        except TagNotFoundException as e:
            logger.warning(f"Попытка удаления несуществующего тега: {tag_id}")
            raise
        except TagInUseException as e:
            logger.warning(
                f"Попытка удаления используемого тега: {tag_id}. "
                f"Используется в {tag['usage_count']} статьях"
            )
            raise
        except Exception as e:
            logger.error(f"Ошибка при удалении тега {tag_id}: {str(e)}")
            raise TagDeletionException(tag_id)

    async def get_tags(
        self, 
        search: Optional[str] = None, 
        limit: int = 20, 
        offset: int = 0
    ) -> TagList:
        """Получить список тегов."""
        try:
            # Валидация параметров
            if limit > 100:
                limit = 100

            # Проверка кэша
            cache_key = await self._get_cache_key(f"list:{search}:{limit}:{offset}")
            cached_data = await self.cache.get(cache_key)
            if cached_data:
                return TagList(**cached_data)

            # Получение данных из БД
            tags = await self.tag_repo.get_tags(search, limit, offset)
            total = await self.tag_repo.get_tags_count(search)

            result = TagList(
                items=[Tag(**tag) for tag in tags],
                total=total
            )

            # Кэширование результата
            await self.cache.set(cache_key, result.model_dump(), self.cache_ttl)
            return result

        except Exception as e:
            logger.error(f"Ошибка при получении списка тегов: {str(e)}")
            raise