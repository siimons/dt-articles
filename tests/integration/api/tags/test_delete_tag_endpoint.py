import pytest
from httpx import AsyncClient
from fastapi import status

from app.api.v1.exceptions import (
    TagNotFoundException,
    TagInUseException,
    TagDeletionException,
)


@pytest.mark.asyncio
async def test_delete_tag_success(client: AsyncClient, create_test_tag):
    """
    Тест успешного удаления тега.
    Должен вернуть 204 NO CONTENT.
    """
    tag = await create_test_tag("python")

    response = await client.delete(f"/api/v1/tags/{tag['id']}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content


@pytest.mark.asyncio
async def test_delete_nonexistent_tag(client: AsyncClient):
    """
    Тест удаления несуществующего тега.
    Должен вернуть 404 NOT FOUND.
    """
    non_existent_tag_id = 9999
    response = await client.delete(f"/api/v1/tags/{non_existent_tag_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == TagNotFoundException(tag_id=non_existent_tag_id).message


# @pytest.mark.asyncio
# async def test_delete_tag_in_use(client: AsyncClient, create_test_tag, create_test_article):
#     """
#     Тест удаления используемого тега.
#     Должен вернуть 400 BAD REQUEST.
#     """
#     tag = await create_test_tag("python")
#     article = await create_test_article(title="Test Article", content="Content", tags=[tag["id"]])

#     response = await client.delete(f"/api/v1/tags/{tag['id']}")

#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert response.json()["detail"] == TagInUseException(tag_id=tag["id"]).message


@pytest.mark.asyncio
async def test_delete_tag_server_error(client: AsyncClient, create_test_tag, mocker):
    """
    Тест обработки внутренней ошибки сервера при удалении тега.
    Должен вернуть 500 INTERNAL SERVER ERROR.
    """
    tag = await create_test_tag("python")

    mocker.patch(
        "app.api.v1.tags.repositories.TagRepository.delete_tag",
        side_effect=Exception("Database error")
    )

    response = await client.delete(f"/api/v1/tags/{tag['id']}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == TagDeletionException(tag_id=tag["id"]).message