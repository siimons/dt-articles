from typing import Optional, List

from app.api.storage.database import Database


class TagRepository:
    """Репозиторий для работы с тегами в базе данных."""

    def __init__(self, db: Database):
        self.db = db

    async def get_tag_by_id(self, tag_id: int) -> Optional[dict]:
        """Получить тег по ID."""
        query = """
        SELECT 
            t.id, 
            t.name, 
            t.created_at, 
            t.updated_at,
            COUNT(at.article_id) as usage_count
        FROM tags t
        LEFT JOIN article_tags at ON t.id = at.tag_id
        WHERE t.id = %s
        GROUP BY t.id, t.name, t.created_at, t.updated_at
        """
        tags = await self.db.fetch(query, tag_id)
        return tags[0] if tags else None

    async def get_tag_by_name(self, name: str) -> Optional[dict]:
        """Получить тег по имени."""
        query = """
        SELECT 
            t.id, 
            t.name, 
            t.created_at, 
            t.updated_at,
            COUNT(at.article_id) as usage_count
        FROM tags t
        LEFT JOIN article_tags at ON t.id = at.tag_id
        WHERE t.name = %s
        GROUP BY t.id, t.name, t.created_at, t.updated_at
        """
        tags = await self.db.fetch(query, name.lower())
        return tags[0] if tags else None

    async def create_tag(self, name: str) -> int:
        """Создать новый тег и вернуть его ID."""
        query = "INSERT INTO tags (name) VALUES (%s)"
        last_id = await self.db.execute(query, name.lower())
        return last_id

    async def delete_tag(self, tag_id: int) -> bool:
        """Удалить тег."""
        query = "DELETE FROM tags WHERE id = %s"
        affected_rows = await self.db.execute(query, tag_id)
        return affected_rows > 0

    async def get_tags(
        self, 
        search: Optional[str] = None, 
        limit: int = 20, 
        offset: int = 0
    ) -> List[dict]:
        """Получить список тегов."""
        query = """
        SELECT 
            t.id, 
            t.name,
            t.created_at,
            t.updated_at,
            COUNT(at.article_id) as usage_count
        FROM tags t
        LEFT JOIN article_tags at ON t.id = at.tag_id
        WHERE %(search)s IS NULL OR t.name LIKE %(search_pattern)s
        GROUP BY t.id, t.name, t.created_at, t.updated_at
        ORDER BY t.name
        LIMIT %(limit)s OFFSET %(offset)s
        """
        params = {
            "search": search,
            "search_pattern": f"%{search}%" if search else None,
            "limit": limit,
            "offset": offset
        }
        return await self.db.fetch(query, params)

    async def get_tags_count(self, search: Optional[str] = None) -> int:
        """Получить общее количество тегов."""
        query = """
        SELECT COUNT(*) as count
        FROM tags
        WHERE %(search)s IS NULL OR name LIKE %(search_pattern)s
        """
        params = {
            "search": search,
            "search_pattern": f"%{search}%" if search else None
        }
        result = await self.db.fetch_one(query, params)
        return result["count"] if result else 0

    async def is_tag_used(self, tag_id: int) -> bool:
        """Проверить, используется ли тег в статьях."""
        query = "SELECT EXISTS(SELECT 1 FROM article_tags WHERE tag_id = %s) as is_used"
        result = await self.db.fetch_one(query, tag_id)
        return result["is_used"] if result else False