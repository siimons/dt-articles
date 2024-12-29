from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the article")
    content: str = Field(..., min_length=1, description="Content of the article")
    tags: List[str] = Field(..., min_items=1, description="List of tags associated with the article")

    class Config:
        str_strip_whitespace = True


class ArticleCreate(ArticleBase):
    """Схема для создания статьи (черновик)"""
    pass


class ArticleUpdate(ArticleBase):
    """Схема для обновления статьи"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated title of the article")
    content: Optional[str] = Field(None, min_length=1, description="Updated content of the article")
    tags: Optional[List[str]] = None

    class Config:
        str_strip_whitespace = True


class ArticleDelete(BaseModel):
    """Схема для удаления статьи"""
    id: int = Field(..., description="ID of the article to be deleted")


class ArticleIDs(BaseModel):
    """Схема для получения всех ID статей"""
    ids: List[int] = Field(..., description="List of article IDs")


class Article(ArticleBase):
    """Схема для получения информации о статье"""
    id: int = Field(..., description="ID of the article")
    created_at: datetime = Field(..., description="Timestamp of when the article was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp of when the article was last updated")
    