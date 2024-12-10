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

class ArticleService:
    def __init__(self, database: Database):
        self.database = database

    async def create_article(self, article: ArticleCreate) -> Article:
        try:
            created_article = await create_article(article)
            if not created_article:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось создать статью. Попробуйте позже."
                )
            return Article(**created_article)
        except ArticleAlreadyExistsException as e:
            raise article_already_exists_exception(article.title)