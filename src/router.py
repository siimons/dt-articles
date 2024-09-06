from fastapi import APIRouter
from datetime import datetime

from src.schemes import ArticleCreate
from src.service import add_article_with_tags 
 
from src.schemes import ArticleUpdate
from src.service import update_article_and_tags 

from src.schemes import ArticleDelete
from src.service import delete_article_from_db

router = APIRouter() 
 
@router.post('/articles/')
def create_article(article: ArticleCreate):

    result = add_article_with_tags(article.title, article.content, article.tags, article.updated_at)
    
    return result

@router.put('/articles/{id}')
def update_article(article: ArticleUpdate):
    
    result = update_article_and_tags(article.id, article.title, article.contents, article.tags, article.updated_at)
    
    return result

@router.delete('/articles/{id}')
def delete_article(article: ArticleDelete):
    
    result = delete_article_from_db(article.id)
    
    return result