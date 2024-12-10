from fastapi import APIRouter, HTTPException, Depends, status

from app.api.v1.services import ArticleService
from app.core.database import Database

from app.api.v1.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    ArticleIDs,
    Article
)

from app.api.v1.exceptions import (
    ArticleAlreadyExistsException,
    InvalidArticleDataException,
    article_already_exists_exception,
    invalid_article_data_exception
)

router = APIRouter()

def get_database() -> Database:
    return Database()

def get_article_service(db: Database = Depends(get_database)) -> ArticleService:
    return ArticleService(database=db)

@router.post("/articles", response_model=Article, status_code=status.HTTP_201_CREATED)
async def create_article_endpoint(
    article: ArticleCreate,
    service: ArticleService = Depends(get_article_service)
):
    """
    Создание новой статьи.

    - **title**: Заголовок статьи
    - **content**: Содержимое статьи
    - **tags**: Список тегов для статьи
    """
    try:
        if not article.title or not article.content or not article.tags:
            raise invalid_article_data_exception("Поля 'title', 'content' и 'tags' обязательны для заполнения.")
        saved_article = await service.create_article(article)
        if not saved_article:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать статью. Пожалуйста, попробуйте снова."
            )
        return saved_article
    except HTTPException as e:
        raise e
    except ArticleAlreadyExistsException as e:
        raise article_already_exists_exception(article.title)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при создании статьи: {str(e)}"
        )