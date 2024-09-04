from fastapi import FastAPI

# Импорт схем для создания постов
from src.schemes import PostCreate, PostResponse

app = FastAPI()

# Тут нужна база данных для хранения постов 

@app.post('/posts/')
def create_post(post: PostCreate):
    new_post = {}
    
    return new_post
