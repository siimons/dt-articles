from app.core.database import Database
from app.api.v1.schemas import ArticleCreate
from app.api.v1.exceptions import ArticleAlreadyExistsException

from app.core.logging import logger


async def create_article(db: Database, article: ArticleCreate) -> dict:
    """
    Создание новой статьи и привязка её к тегам.
    """
    query_check = "SELECT id FROM articles WHERE title = %s"
    existing_article = await db.fetch(query_check, article.title)

    if existing_article:
        logger.error(f"Статья с заголовком '{article.title}' уже существует.")
        raise ArticleAlreadyExistsException(article.title)

    await db.start_transaction()

    try:
        query_create_article = """
        INSERT INTO articles (title, content)
        VALUES (%s, %s)
        """
        await db.execute(query_create_article, article.title, article.content)

        query_get_article_id = "SELECT LAST_INSERT_ID() AS id"
        article_id_result = await db.fetch(query_get_article_id)
        article_id = article_id_result[0]["id"]

        logger.success(f"Статья '{article.title}' успешно создана с ID {article_id}.")

        if article.tags:
            tag_ids = await _ensure_tags_exist(db, article.tags)

            await _associate_tags_with_article(db, article_id, tag_ids)

        await db.commit_transaction()

        return {
            "id": article_id,
            "title": article.title,
            "content": article.content,
            "tags": article.tags,
        }

    except Exception as e:
        await db.rollback_transaction()
        logger.error(f"Ошибка при создании статьи '{article.title}': {e}")
        raise


async def _ensure_tags_exist(db: Database, tags: list[str]) -> list[int]:
    """
    Создаёт новые теги, если они не существуют, и возвращает их IDs.
    """
    tag_ids = []
    for tag in tags:
        query_check_tag = "SELECT id FROM tags WHERE name = %s"
        existing_tag = await db.fetch(query_check_tag, tag)

        if existing_tag:
            tag_ids.append(existing_tag[0]["id"])
        else:
            query_create_tag = "INSERT INTO tags (name) VALUES (%s)"
            await db.execute(query_create_tag, tag)

            query_get_tag_id = "SELECT LAST_INSERT_ID() AS id"
            tag_id_result = await db.fetch(query_get_tag_id)
            tag_ids.append(tag_id_result[0]["id"])

            logger.info(f"Создан новый тег '{tag}' с ID {tag_id_result[0]['id']}.")

    return tag_ids


async def _associate_tags_with_article(db: Database, article_id: int, tag_ids: list[int]) -> None:
    """
    Связывает статью с тегами через таблицу article_tags.
    """
    query_associate = "INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)"
    try:
        for tag_id in tag_ids:
            await db.execute(query_associate, article_id, tag_id)
            logger.info(f"Тег ID {tag_id} связан со статьёй ID {article_id}.")
    except Exception as e:
        logger.error(f"Ошибка при связывании тегов с статьёй ID {article_id}: {e}")
        raise
