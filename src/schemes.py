from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Схема для создания поста
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    published: Optional[bool] = True

# Схема для отображения информации о посте
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True