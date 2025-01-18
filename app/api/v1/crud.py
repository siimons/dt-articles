from app.core.database import Database
from app.api.v1.schemas import ArticleCreate
from app.api.v1.exceptions import ArticleAlreadyExistsException

from app.core.logging import logger

async def create_article(db: Database, article: ArticleCreate) -> dict:
    """
    Создание новой статьи.
    """
    query_check = "SELECT id FROM articles WHERE title = %s"
    existing_article = await db.fetch(query_check, article.title)
    
    if existing_article:
        logger.error(f"Статья с заголовком '{article.title}' уже существует.")
        raise ArticleAlreadyExistsException(article.title)

    query_create = """
    INSERT INTO articles (title, content, tags)
    VALUES (%s, %s, %s)
    """
    try:
        new_article = await db.fetch(query_create, article.title, article.content, article.tags)
        logger.success(f"Статья '{article.title}' успешно создана.")
        return new_article[0]
    except Exception as e:
        logger.error(f"Ошибка при создании статьи '{article.title}': {e}")
        raise