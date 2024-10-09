from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    tags: List[str]
'''Схема для создания статьи'''

class ArticleUpdate(BaseModel):
    id: int
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    contents: Optional[str] = Field(None, min_lenght=1)
    tags: List[str]
'''Схема для изменения статьи''' 

class ArticleDelete(BaseModel):
    id: int
'''Схема для удаления статьи'''
    
class ArticleIDs(BaseModel):
    ids: List[int]
'''Схема для получения всей id статей'''
    
class Article(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None
'''Схема для получения какой-то отдельной статьи'''