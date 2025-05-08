from fastapi import Depends

from app.api.storage.database import Database
from app.api.v1.tags.repositories import TagRepository

from app.core.dependencies.common import get_database


async def get_tag_repository(
    db: Database = Depends(get_database),
) -> TagRepository:
    """
    Dependency для получения репозитория тегов.

    Args:
        db (Database): Объект базы данных.

    Returns:
        TagRepository: Репозиторий тегов.
    """
    return TagRepository(db)
