from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
'''Схема для создания нового пользователя'''

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
'''Схема для отображения информации о пользователе'''

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=6)
'''Схема для обновления данных пользователя'''

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