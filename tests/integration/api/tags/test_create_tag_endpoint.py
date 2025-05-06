import pytest
from httpx import AsyncClient
from fastapi import status

from app.api.v1.exceptions import TagAlreadyExistsException


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
    assert "id" in response_data
    assert response_data["usage_count"] == 0


@pytest.mark.asyncio
async def test_create_tag_duplicate(client: AsyncClient):
    """
    Тест создания дубликата тега.
    Должен вернуть 400 BAD REQUEST с сообщением о существующем теге.
    """
    tag_data = {"name": "python"}

    response = await client.post("/api/v1/tags", json=tag_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post("/api/v1/tags", json=tag_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == TagAlreadyExistsException(tag_name="python").message


@pytest.mark.asyncio
async def test_create_tag_invalid_name(client: AsyncClient):
    """
    Тест создания тега с невалидным именем.
    Должен вернуть 422 UNPROCESSABLE ENTITY.
    """
    test_cases = [
        ({"name": "p"}, ["string_too_short"]),
        ({"name": "a" * 51}, ["string_too_long"]),
        ({"name": "python!"}, ["value_error"]),
        ({"name": " python "}, ["value_error"]),
    ]

    for data, expected_errors in test_cases:
        response = await client.post("/api/v1/tags", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        error_types = [error["type"] for error in response.json().get("detail", [])]

        for expected_error in expected_errors:
            assert expected_error in error_types, \
                f"Для данных {data} ожидалась ошибка {expected_error}, получены {error_types}"


@pytest.mark.asyncio
async def test_create_tag_case_insensitive(client: AsyncClient):
    """
    Тест регистронезависимости при создании тега.
    Должен считать 'Python' и 'python' одинаковыми тегами.
    """
    response = await client.post("/api/v1/tags", json={"name": "python"})
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post("/api/v1/tags", json={"name": "Python"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == TagAlreadyExistsException(tag_name="python").message


@pytest.mark.asyncio
async def test_create_tag_empty_name(client: AsyncClient):
    """
    Тест создания тега с пустым именем.
    Должен вернуть 422 UNPROCESSABLE ENTITY.
    """
    response = await client.post("/api/v1/tags", json={"name": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(error["type"] == "string_too_short" 
              for error in response.json()["detail"])


@pytest.mark.asyncio
async def test_create_tag_missing_name(client: AsyncClient):
    """
    Тест создания тега без указания имени.
    Должен вернуть 422 UNPROCESSABLE ENTITY.
    """
    response = await client.post("/api/v1/tags", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(error["type"] == "missing" 
              for error in response.json()["detail"])
