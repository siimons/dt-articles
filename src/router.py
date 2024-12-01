from fastapi import APIRouter, HTTPException

from src.exceptions import (
    ArticleNotFoundException,
    ArticleAlreadyExistsException,
    ArticleDeletionException,
    InvalidArticleDataException,
    article_not_found_exception,
    article_already_exists_exception,
    article_deletion_exception,
    invalid_article_data_exception
)

from src.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    ArticleIDs,
    Article
)

from src.service import (
    add_article_with_tags,
    update_article_and_tags,
    delete_article_from_db, 
    get_all_article_ids,
    get_article_by_id
)

router = APIRouter()

@router.post('/api/article/')
def create_article(article: ArticleCreate):
    try:
        result = add_article_with_tags(article.title, article.content, article.tags)
        return result
    except ArticleAlreadyExistsException as e:
        raise article_already_exists_exception(article.title)
    except InvalidArticleDataException as e:
        raise invalid_article_data_exception(str(e))

@router.put('/api/article/{id}')
def update_article(id: int, article: ArticleUpdate):
    try:
        result = update_article_and_tags(id, article.title, article.content, article.tags, article.updated_at)
        return result
    except ArticleNotFoundException as e:
        raise article_not_found_exception(id)
    except InvalidArticleDataException as e:
        raise invalid_article_data_exception(str(e))

@router.delete('/api/article/{id}')
def delete_article(id: int):
    try:
        result = delete_article_from_db(id)
        return result
    except ArticleNotFoundException as e:
        raise article_not_found_exception(id)
    except ArticleDeletionException as e:
        raise article_deletion_exception(id)

@router.get('/api/articles/ids', response_model=ArticleIDs)
def fetch_article_ids():
    try:
        article_ids = get_all_article_ids()
        return ArticleIDs(ids=article_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении статей.")

@router.get('/api/article/{article_id}', response_model=Article)
def read_article(article_id: int):
    try:
        result = get_article_by_id(article_id)
        return result
    except ArticleNotFoundException as e:
        raise article_not_found_exception(article_id)
