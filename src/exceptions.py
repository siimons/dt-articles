from fastapi import HTTPException

class ArticleBaseException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
'''Базовое исключение для статей'''

class ArticleNotFoundException(ArticleBaseException):
    def __init__(self, article_id: int):
        message = f"Статья с ID {article_id} не найдена."
        super().__init__(message)
'''Исключение для ситуации, когда статья не найдена'''

class ArticleAlreadyExistsException(ArticleBaseException):
    def __init__(self, title: str):
        message = f"Статья с названием '{title}' уже существует."
        super().__init__(message)
'''Исключение для ситуации, когда статья с таким названием уже существует'''

class ArticleUpdateException(ArticleBaseException):
    def __init__(self, article_id: int):
        message = f"Ошибка при обновлении статьи с ID {article_id}."
        super().__init__(message)
'''Исключение для ошибки обновления статьи'''

class ArticleDeletionException(ArticleBaseException):
    def __init__(self, article_id: int):
        message = f"Ошибка при удалении статьи с ID {article_id}."
        super().__init__(message)
'''Исключение для ошибки удаления статьи'''

class InvalidArticleDataException(ArticleBaseException):
    def __init__(self, detail: str):
        message = f"Недопустимые данные статьи: {detail}."
        super().__init__(message)
'''Исключение для ошибки недопустимых данных'''

def article_not_found_exception(article_id: int):
    return HTTPException(status_code=404, detail=f"Статья с ID {article_id} не найдена.")

def article_already_exists_exception(title: str):
    return HTTPException(status_code=400, detail=f"Статья с заголовком '{title}' уже существует.")

def article_deletion_exception(article_id: int):
    return HTTPException(status_code=500, detail=f"Ошибка при удалении статьи с ID {article_id}.")

def invalid_article_data_exception(detail: str):
    return HTTPException(status_code=422, detail=f"Недопустимые данные статьи: {detail}.")
'''Функции для обработки исключений в HTTP-ответы'''