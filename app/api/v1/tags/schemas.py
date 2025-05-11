from typing import Annotated
from datetime import datetime

from pydantic.functional_serializers import PlainSerializer
from pydantic import BaseModel, ConfigDict, Field, field_validator


DateTimeIso = Annotated[
    datetime,
    PlainSerializer(lambda v: v.isoformat(), return_type=str)
]


class TagBase(BaseModel):
    """Базовая схема для тега."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Название тега (2-50 символов, только буквы, цифры и дефисы)"
    )

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Валидация названия тега."""
        if not v.replace('-', '').isalnum():
            raise ValueError(
                "Название тега должно содержать только буквы, цифры и дефисы"
            )
        return v.lower()


class TagCreate(TagBase):
    """Схема для создания тега."""
    pass


class TagUpdate(BaseModel):
    """Схема для обновления тега."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Новое название тега (2-50 символов, только буквы, цифры и дефисы)"
    )

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Валидация названия тега."""
        if not v.replace('-', '').isalnum():
            raise ValueError(
                "Название тега должно содержать только буквы, цифры и дефисы"
            )
        return v.lower()


class Tag(TagBase):
    """Схема для отображения информации о теге."""

    id: int = Field(..., description="Уникальный идентификатор тега")
    created_at: DateTimeIso = Field(
        ...,
        description="Дата и время создания тега"
    )
    updated_at: DateTimeIso = Field(
        ...,
        description="Дата и время последнего обновления тега"
    )
    usage_count: int = Field(
        0,
        description="Количество статей, использующих этот тег"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "python",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "usage_count": 42
            }
        }
    )


class TagList(BaseModel):
    """Схема для списка тегов."""

    items: list[Tag] = Field(..., description="Список тегов")
    total: int = Field(..., description="Общее количество тегов")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "python",
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-01T00:00:00",
                        "usage_count": 42
                    }
                ],
                "total": 1
            }
        }
    )