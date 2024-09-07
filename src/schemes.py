from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Схема для создания нового пользователя
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

# Схема для отображения информации о пользователе
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

# Схема для обновления данных пользователя
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=6)

# Схема для создания статьи
class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    tags: List[str]
    updated_at: datetime

# Схема для изменения статьи 
class ArticleUpdate(BaseModel):
    id: int
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    contents: Optional[str] = Field(None, min_lenght=1)
    tags: List[str]
    updated_at: datetime

# Схема для удаления статьи
class ArticleDelete(BaseModel):
    id: int
    
# Схема для получения всей id статей
class ArticleIDs(BaseModel):
    ids: List[int]
    
# Схема для получения какой-то отдельной статьи
class Article(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime] = None