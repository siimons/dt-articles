from fastapi import APIRouter, Depends, status

from app.core.database import Database
from app.core.dependencies import get_database
from app.api.v1.services import ArticleService

from app.api.v1.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    ArticleIDs,
    Article
)

router = APIRouter()
article_service = ArticleService()

@router.post("/articles", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_article_endpoint(
    article_data: ArticleCreate,
    db: Database = Depends(get_database)
):
    """
    Создание новой статьи.
    ---
    - **title**: Заголовок статьи.
    - **content**: Содержимое статьи.
    - **tags**: Список тегов.
    """
    return await article_service.process_article_creation(db, article_data)