from fastapi import APIRouter, HTTPException, status

from app.api.exceptions import (
    ArticleAlreadyExistsException,
    InvalidArticleDataException,
    article_already_exists_exception,
    invalid_article_data_exception
)

from app.api.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    ArticleIDs,
    Article
)

router = APIRouter()

@router.post("/api/articles", response_model=Article, status_code=status.HTTP_201_CREATED)
async def create_article(article: ArticleCreate):
    """
    Создание новой статьи.
    
    - **title**: Заголовок статьи
    - **content**: Содержимое статьи
    - **tags**: Список тегов для статьи
    """
    try:
        saved_article = await save_article_to_db(article)
        
        return saved_article
    
    except ArticleAlreadyExistsException as e:
        raise article_already_exists_exception(article.title)
    
    except InvalidArticleDataException as e:
        raise invalid_article_data_exception(str(e))
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при создании статьи: {str(e)}"
        )