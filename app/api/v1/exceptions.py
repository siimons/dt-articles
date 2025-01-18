from fastapi import HTTPException


class ArticleBaseException(Exception):
    """Базовое исключение для всех ошибок, связанных с статьями"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ArticleNotFoundException(ArticleBaseException):
    """Исключение для ситуации, когда статья не найдена"""
    
    def __init__(self, article_id: int):
        message = f"Статья с ID {article_id} не найдена."
        super().__init__(message)


class ArticleAlreadyExistsException(ArticleBaseException):
    """Исключение для ситуации, когда статья с таким названием уже существует"""
    
    def __init__(self, title: str):
        message = f"Статья с названием \'{title}\' уже существует."
        super().__init__(message)


class ArticleUpdateException(ArticleBaseException):
    """Исключение для ошибки при обновлении статьи"""
    
    def __init__(self, article_id: int):
        message = f"Ошибка при обновлении статьи с ID {article_id}."
        super().__init__(message)


class ArticleDeletionException(ArticleBaseException):
    """Исключение для ошибки удаления статьи"""
    
    def __init__(self, article_id: int):
        message = f"Ошибка при удалении статьи с ID {article_id}."
        super().__init__(message)


class InvalidArticleDataException(ArticleBaseException):
    """Исключение для недопустимых данных статьи"""
    
    def __init__(self, detail: str):
        message = f"Недопустимые данные статьи: {detail}."
        super().__init__(message)


def article_not_found_exception(article_id: int):
    """Обрабатывает исключение, когда статья не найдена"""
    return HTTPException(
        status_code=404,
        detail=f"Статья с ID {article_id} не найдена."
    )


def article_already_exists_exception(title: str):
    """Обрабатывает исключение, когда статья с таким названием уже существует"""
    return HTTPException(
        status_code=409,
        detail=f"Статья с заголовком \'{title}\' уже существует."
    )


def article_update_exception(article_id: int):
    """Обрабатывает исключение при ошибке обновления статьи"""
    return HTTPException(
        status_code=500,
        detail=f"Ошибка при обновлении статьи с ID {article_id}."
    )


def article_deletion_exception(article_id: int):
    """Обрабатывает исключение при ошибке удаления статьи"""
    return HTTPException(
        status_code=500,
        detail=f"Ошибка при удалении статьи с ID {article_id}."
    )


def invalid_article_data_exception(detail: str):
    """Обрабатывает исключение при недопустимых данных статьи"""
    return HTTPException(
        status_code=422,
        detail=f"Недопустимые данные статьи: {detail}."
    )
