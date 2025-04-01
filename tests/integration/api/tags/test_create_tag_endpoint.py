import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_create_tag_success(client: AsyncClient):
    """
    Тест успешного создания тега.
    Должен вернуть 201 CREATED и корректные данные тега.
    """
    tag_data = {"name": "python"}
    response = await client.post("/api/v1/tags", json=tag_data)

    assert response.status_code == status.HTTP_201_CREATED, f"Ошибка: {response.text}"

    response_data = response.json()
    assert response_data["name"] == tag_data["name"].lower()
    assert "id" in response_data, "Ответ должен содержать ID тега"
    assert response_data["usage_count"] == 0, "Новый тег не должен использоваться"
