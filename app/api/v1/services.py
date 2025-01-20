from fastapi import HTTPException, status

from app.core.database import Database
from app.api.v1.crud import create_article

from app.api.v1.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    ArticleIDs,
    Article
)

from app.api.v1.exceptions import (
    ArticleAlreadyExistsException,
    article_already_exists_exception
)

from app.core.logging import logger


class ArticleService:
    async def process_article_creation(self, db: Database, article_data: ArticleCreate) -> dict:
        """
        Обработка создания новой статьи.
        """
        try:
            logger.info(f"Попытка создания статьи с заголовком: {article_data.title}")
            new_article = await create_article(db, article_data)
            logger.success(f"Статья '{new_article['title']}' успешно создана.")
            return new_article
        except ArticleAlreadyExistsException:
            logger.error(f"Статья с заголовком '{article_data.title}' уже существует.")
            raise article_already_exists_exception(article_data.title)
        except Exception as e:
            logger.error(f"Неизвестная ошибка при создании статьи '{article_data.title}': {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании статьи."
            )