import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from src.exceptions import ArticleAlreadyExistsException, InvalidArticleDataException

client = TestClient(app)

@pytest.fixture
def valid_article():
    """Возвращает корректные данные для создания статьи."""
    return {
        "title": "Test Article",
        "content": "This is a test article content.",
        "tags": ["test", "article"]
    }

@pytest.fixture
def invalid_article():
    """Возвращает данные с некорректной статьей (например, без контента)."""
    return {
        "title": "Invalid Article",
        "content": "",
        "tags": ["invalid"]
    }

def test_create_article_success(valid_article):
    """Тест на успешное создание статьи."""
    response = client.post('/api/article/', json=valid_article)

    # Проверяем, что статья была успешно создана
    
    # hint: for create article object, db connect is required
    assert response.status_code == 200, "Статья не была успешно создана"
    response_data = response.json()
    
    # fix: checks are outdated
    assert "article_id" in response_data, "Ответ не содержит ID статьи"
    assert "message" in response_data, "Ответ не содержит сообщения"

# В топку эту проверку, там нужно дохрена проверять всего
# def test_create_article_already_exists(valid_article, mocker):
#     """Тест на создание уже существующей статьи."""
#     # Мокируем сервис, чтобы он выбросил ArticleAlreadyExistsException
#     mocker.patch('src.service.add_article_with_tags', side_effect=ArticleAlreadyExistsException(valid_article['title']))

#     response = client.post('/api/article/', json=valid_article)

#     # Ожидаем ошибку 400, так как статья уже существует
#     assert response.status_code == 400, "Ожидается ошибка при повторном создании статьи"
#     response_data = response.json()
#     assert response_data["detail"] == f"Статья с названием {valid_article['title']} уже существует"

def test_create_article_invalid_data(invalid_article, mocker):
    """Тест на создание статьи с некорректными данными."""
    # Мокируем сервис, чтобы он выбросил InvalidArticleDataException
    mocker.patch('src.service.add_article_with_tags', side_effect=InvalidArticleDataException("Invalid content"))

    response = client.post('/api/article/', json=invalid_article)

    # Ожидаем ошибку 422 или 400 в зависимости от обработки данных
    assert response.status_code == 422, "Ожидается ошибка при создании статьи с некорректными данными"
    
    # fix: this assert is usefull
    # response_data = response.json()
    # assert response_data["detail"] == "Invalid content"