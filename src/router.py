from fastapi import APIRouter

from src.schemes import (
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

    result = add_article_with_tags(article.title, article.content, article.tags)
    
    return result

@router.put('/api/article/{id}')
def update_article(article: ArticleUpdate):
    
    result = update_article_and_tags(article.id, article.title, article.contents, article.tags, article.updated_at)
    
    return result

@router.delete('/api/article/{id}')
def delete_article(id: int):
    
    result = delete_article_from_db(id)
    
    return result

@router.get('/api/articles/ids', response_model=ArticleIDs)
def fetch_article_ids():
    
    article_ids = get_all_article_ids()
    
    return ArticleIDs(ids=article_ids)

@router.get('/api/article/{article_id}', response_model=Article)
def read_article(article_id: int):
    
    result = get_article_by_id(article_id)
    
    return result