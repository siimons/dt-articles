from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from app.api.v1.tags.services import TagService

from app.core.dependencies.services import get_tag_service
# from app.api.security.rate_limiter import get_rate_limiter

from app.api.v1.tags.schemas import (
    TagCreate,
    Tag,
    TagList,
)

tags_router = APIRouter(prefix="/api/v1/tags", tags=["Tags"])


@tags_router.post(
    "",
    response_model=Tag,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый тег",
    description="Создает новый тег. Доступно только администраторам.",
    responses={
        400: {"description": "Тег с таким именем уже существует"},
        422: {"description": "Ошибка валидации данных"},
        500: {"description": "Ошибка при создании тега"}
    }
)
# @get_rate_limiter().limit("10/minute")
async def create_tag_endpoint(
    tag_data: TagCreate,
    tag_service: TagService = Depends(get_tag_service),
):
    """Создать новый тег."""
    return await tag_service.create_tag(tag_data)


@tags_router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тег",
    description="Удаляет тег по ID. Доступно только администраторам.",
    responses={
        404: {"description": "Тег не найден"},
        400: {"description": "Тег используется в статьях"},
        500: {"description": "Ошибка при удалении тега"}
    }
)
# @get_rate_limiter().limit("10/minute")
async def delete_tag_endpoint(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
):
    """Удалить тег."""
    await tag_service.delete_tag(tag_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


@tags_router.get(
    "",
    response_model=TagList,
    status_code=status.HTTP_200_OK,
    summary="Получить список тегов",
    description="Возвращает список всех тегов с возможностью поиска и пагинации.",
    responses={
        200: {"description": "Успешный запрос"},
        500: {"description": "Ошибка при получении списка тегов"}
    }
)
# @get_rate_limiter().limit("60/minute")
async def get_tags_endpoint(
    search: Optional[str] = Query(
        None, 
        min_length=2,
        description="Фильтр по названию тега (поиск по подстроке, минимум 2 символа)"
    ),
    limit: int = Query(
        20, 
        ge=1, 
        le=100, 
        description="Ограничение количества тегов (максимум 100)"
    ),
    offset: int = Query(
        0, 
        ge=0, 
        description="Смещение для пагинации"
    ),
    tag_service: TagService = Depends(get_tag_service),
):
    """Получить список тегов."""
    return await tag_service.get_tags(search, limit, offset)
