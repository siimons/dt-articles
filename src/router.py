from fastapi import APIRouter
from datetime import datetime

from src.schemes import ArticleCreate
from src.service import add_article_with_tags 
 
from src.schemes import ArticleUpdate
from src.service import update_article_and_tags 

from src.schemes import ArticleDelete
from src.service import delete_article_from_db

from src.schemes import ArticleIDs
from src.service import get_all_article_ids

from src.schemes import Article
from src.service import get_article_by_id

router = APIRouter() 
 
@router.post('/article/')
def create_article(article: ArticleCreate):

    result = add_article_with_tags(article.title, article.content, article.tags, article.updated_at)
    
    return result

@router.put('/article/{id}')
def update_article(article: ArticleUpdate):
    
    result = update_article_and_tags(article.id, article.title, article.contents, article.tags, article.updated_at)
    
    return result

@router.delete('/article/{id}')
def delete_article(article: ArticleDelete):
    
    result = delete_article_from_db(article.id)
    
    return result

@router.get('/articles/ids', response_model=ArticleIDs)
def fetch_article_ids():
    
    article_ids = get_all_article_ids()
    
    return ArticleIDs(ids=article_ids)

@router.get('/article/{article_id}', response_model=Article)
def read_article(article_id: int):
    
    result = get_article_by_id(article_id)
    
    return result