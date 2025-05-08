from fastapi import Depends

from app.api.storage.redis import RedisManager
from app.api.v1.tags.repositories import TagRepository
from app.api.v1.tags.services import TagService

from app.core.dependencies.repositories import get_tag_repository
from app.core.dependencies.common import get_cache


async def get_tag_service(
    tag_repo: TagRepository = Depends(get_tag_repository),
    cache: RedisManager = Depends(get_cache),
) -> TagService:
    """
    Dependency для получения сервиса тегов.

    Args:
        tag_repo (TagRepository): Репозиторий тегов.
        cache (RedisManager): Объект кэша.

    Returns:
        TagService: Сервис тегов.
    """
    return TagService(tag_repo, cache)
