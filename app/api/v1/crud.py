from app.core.database import Database
from app.api.v1.schemas import ArticleCreate
from app.api.v1.exceptions import ArticleAlreadyExistsException

db = Database()

async def create_article(article: ArticleCreate) -> dict:
    query = """
    INSERT INTO articles (title, content, tags) 
    VALUES (%s, %s, %s) RETURNING id, title, content, tags, created_at;
    """
    existing_article = await db.fetch("SELECT * FROM articles WHERE title = %s;", article.title)
    if existing_article:
        raise ArticleAlreadyExistsException(article.title)

    result = await db.fetch(query, article.title, article.content, article.tags)
    if not result:
        return None
    return result[0]