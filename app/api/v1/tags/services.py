from typing import Optional

from app.api.v1.tags.repositories import TagRepository
from app.api.storage.redis import RedisManager

from app.api.v1.tags.schemas import (
    TagCreate,
    Tag,
    TagList,
)

from app.api.v1.exceptions import (
    ServiceException,
    TagAlreadyExistsException,
    TagNotFoundException,
    TagInUseException,
    TagDeletionException,
    TagValidationException,
)

from app.core.logging import logger


class TagService:
    """Сервис для управления тегами с кэшированием."""

    def __init__(self, tag_repo: TagRepository, cache: RedisManager):
        self.tag_repo = tag_repo
        self.cache = cache
        self.cache_prefix = "tag:"
        self.cache_ttl = 3600 # 1 час

    async def _get_cache_key(self, key: str) -> str:
        """Генерирует ключ для кэша."""
        return f"{self.cache_prefix}{key}"

    async def _invalidate_tag_cache(self, tag_id: int, tag_name: str) -> None:
        """Инвалидирует кэш для тега."""
        await self.cache.delete(await self._get_cache_key(f"id:{tag_id}"))
        await self.cache.delete(await self._get_cache_key(f"name:{tag_name}"))
        await self.cache.delete(await self._get_cache_key("list:all"))

    async def create_tag(self, tag_data: TagCreate) -> Tag:
        """Создать новый тег."""
        try:
            existing_tag = await self.tag_repo.get_tag_by_name(tag_data.name)
            if existing_tag:
                logger.warning(f"Попытка создания дубликата тега: {tag_data.name}")
                raise TagAlreadyExistsException(tag_data.name)

            tag_id = await self.tag_repo.create_tag(tag_data.name)
            if not tag_id:
                logger.error("Не удалось создать тег: не получен ID")
                raise TagValidationException("Не удалось создать тег")

            tag = await self.tag_repo.get_tag_by_id(tag_id)
            if not tag:
                logger.error(f"Созданный тег не найден: ID {tag_id}")
                raise TagNotFoundException(tag_id)

            logger.info(f"Создан новый тег: {tag['name']} (ID: {tag_id})")
            return Tag(**tag)

        except ValueError as e:
            logger.error(f"Ошибка валидации тега: {str(e)}")
            raise TagValidationException(str(e))
        except ServiceException as e:
            raise e.to_http()
        except Exception as e:
            logger.error(f"Неожиданная ошибка при создании тега: {str(e)}")
            raise TagValidationException("Внутренняя ошибка сервера при создании тега")

    async def delete_tag(self, tag_id: int) -> None:
        """Удалить тег."""
        try:
            tag = await self.tag_repo.get_tag_by_id(tag_id)
            if not tag:
                logger.warning(f"Попытка удаления несуществующего тега: ID {tag_id}")
                raise TagNotFoundException(tag_id)

            is_used = await self.tag_repo.is_tag_used(tag_id)
            logger.info(f"Проверка использования тега {tag_id}: {is_used}")

            if is_used:
                logger.warning(
                    f"Попытка удаления используемого тега: ID {tag_id}. "
                    f"Используется в {tag['usage_count']} статьях"
                )
                raise TagInUseException(tag_id)

            deleted = await self.tag_repo.delete_tag(tag_id)
            if deleted:
                logger.error(f"Ошибка при удалении тега: ID {tag_id}")
                raise TagDeletionException(tag_id)

            await self._invalidate_tag_cache(tag_id, tag["name"])
            logger.info(f"Тег удалён: {tag['name']} (ID: {tag_id})")

        except ServiceException as e:
            raise e.to_http()
        except Exception as e:
            logger.error(f"Неожиданная ошибка при удалении тега {tag_id}: {str(e)}")
            raise TagDeletionException(tag_id).to_http()

    async def get_tags(
        self,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> TagList:
        """Получить список тегов."""
        try:
            validated_limit = min(limit, 100)
            normalized_search = search.strip().lower() if search else None

            cache_key = await self._get_cache_key(
                f"list:{normalized_search}:{validated_limit}:{offset}"
            )

            if cached_data := await self.cache.get(cache_key):
                try:
                    return TagList.model_validate_json(cached_data)
                except Exception as e:
                    logger.warning(f"Невалидные данные в кэше: {str(e)}")
                    await self.cache.delete(cache_key)

            tags = await self.tag_repo.get_tags(normalized_search, validated_limit, offset)
            total_count = await self.tag_repo.get_tags_count(normalized_search)

            result = TagList(
                items=[Tag(**tag) for tag in tags],
                total=total_count
            )

            try:
                await self.cache.set(
                    cache_key,
                    result.model_dump_json(),
                    self.cache_ttl
                )
            except Exception as e:
                logger.error(f"Ошибка записи в кэш: {str(e)}")

            return result

        except ServiceException as e:
            raise e.to_http()
        except Exception as e:
            logger.error(f"Критическая ошибка: {str(e)}")
            raise ServiceException("Сервис временно недоступен", 503)