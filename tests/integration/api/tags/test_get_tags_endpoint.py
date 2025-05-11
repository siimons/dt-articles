import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_tags_empty_list(client: AsyncClient):
    """
    Тест получения пустого списка тегов.
    Должен вернуть 200 OK с пустым списком.
    """
    response = await client.get("/api/v1/tags")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


@pytest.mark.asyncio
async def test_get_tags_with_pagination(
    client: AsyncClient,
    create_test_tag
):
    """
    Тест пагинации при получении списка тегов.
    Должен корректно работать limit и offset.
    """
    tags = []
    for i in range(1, 6):
        tag = await create_test_tag(f"tag{i}")
        tags.append(tag)

    response = await client.get("/api/v1/tags?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "tag1"
    assert data["items"][1]["name"] == "tag2"

    response = await client.get("/api/v1/tags?limit=2&offset=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "tag3"
    assert data["items"][1]["name"] == "tag4"


@pytest.mark.asyncio
async def test_get_tags_search(
    client: AsyncClient,
    create_test_tag
):
    """
    Тест поиска тегов по названию.
    Должен возвращать только теги, соответствующие поисковому запросу.
    """
    await create_test_tag("python")
    await create_test_tag("django")
    await create_test_tag("python-advanced")

    response = await client.get("/api/v1/tags?search=PYTHON")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 2
    assert {tag["name"] for tag in data["items"]} == {"python", "python-advanced"}


@pytest.mark.asyncio
async def test_get_tags_search_min_length(
    client: AsyncClient,
    create_test_tag
):
    """
    Тест минимальной длины поискового запроса.
    Должен возвращать 422 UNPROCESSABLE ENTITY при запросе менее 2 символов.
    """
    await create_test_tag("python")

    response = await client.get("/api/v1/tags?search=p")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(
        error["type"] == "string_too_short" 
        for error in response.json()["detail"]
    )


@pytest.mark.asyncio
async def test_get_tags_limit_validation(client: AsyncClient):
    """
    Тест валидации параметра limit.
    Должен возвращать 422 UNPROCESSABLE ENTITY при некорректных значениях.
    """
    test_cases = [
        ("0", "greater_than_equal"),
        ("101", "less_than_equal"),
        ("-1", "greater_than_equal"),
        ("abc", "int_parsing")
    ]

    for value, error_type in test_cases:
        response = await client.get(f"/api/v1/tags?limit={value}")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert any(
            error["type"] == error_type 
            for error in response.json()["detail"]
        )


@pytest.mark.asyncio
async def test_get_tags_offset_validation(client: AsyncClient):
    """
    Тест валидации параметра offset.
    Должен возвращать 422 UNPROCESSABLE ENTITY при отрицательном значении.
    """
    response = await client.get("/api/v1/tags?offset=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(
        error["type"] == "greater_than_equal" 
        for error in response.json()["detail"]
    )


@pytest.mark.asyncio
async def test_get_tags_sorting(
    client: AsyncClient,
    create_test_tag
):
    """
    Тест сортировки тегов.
    Должен возвращать теги в алфавитном порядке.
    """
    tags_order = ["django", "flask", "python"]
    for name in reversed(tags_order):
        await create_test_tag(name)

    response = await client.get("/api/v1/tags")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert [tag["name"] for tag in data["items"]] == tags_order
