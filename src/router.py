from fastapi import APIRouter
from datetime import datetime

# Импорт схем для создания постов
from src.schemes import PostCreate, PostResponse
from src.service import add_article_with_tags 

router = APIRouter() 

# Функция для создания постов 
@router.post('/posts/')
def create_post(post: PostCreate):

    # Сохраняем пост в базу данных
    result = add_article_with_tags(post.title, post.content, post.tags)
    
    return result
