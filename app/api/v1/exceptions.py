from fastapi import HTTPException


class ServiceException(Exception):
    """Базовый класс для всех исключений сервиса."""

    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code
        super().__init__(message)

    def to_http(self) -> HTTPException:
        """Преобразует исключение в HTTPException."""
        return HTTPException(status_code=self.code, detail=self.message)


# Исключения для статей
class ArticleNotFoundException(ServiceException):
    """Исключение для ситуации, когда статья не найдена."""

    def __init__(self, article_id: int):
        super().__init__(f"Статья с ID {article_id} не найдена.", 404)


class ArticleAlreadyPublishedException(ServiceException):
    """Исключение для ситуации, когда статья уже опубликована."""

    def __init__(self, article_id: int):
        super().__init__(f"Статья с ID {article_id} уже опубликована.", 400)


class ArticleUpdateException(ServiceException):
    """Исключение для ошибки при обновлении статьи."""

    def __init__(self, article_id: int):
        super().__init__(f"Ошибка при обновлении статьи с ID {article_id}.", 500)


class ArticleDeletionException(ServiceException):
    """Исключение для ошибки удаления статьи."""

    def __init__(self, article_id: int):
        super().__init__(f"Ошибка при удалении статьи с ID {article_id}.", 500)


# Исключения для тегов
class TagNotFoundException(ServiceException):
    """Исключение для ситуации, когда тег не найден."""

    def __init__(self, tag_id: int):
        super().__init__(f"Тег с ID {tag_id} не найден.", 404)


class TagAlreadyExistsException(ServiceException):
    """Исключение для ситуации, когда тег с таким именем уже существует."""

    def __init__(self, tag_name: str):
        super().__init__(f"Тег с именем {tag_name} уже существует.", 400)


class TagDeletionException(ServiceException):
    """Исключение для ошибки удаления тега."""

    def __init__(self, tag_id: int):
        super().__init__(f"Ошибка при удалении тега с ID {tag_id}.", 500)
