from fastapi import HTTPException
from datetime import datetime

from src.utils import get_db_connection
from mysql.connector import Error

def add_article_with_tags(title: str, content: str, tags: list[str]) -> dict:
    try:
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor()
            connection.start_transaction()

            insert_article_query = """
            INSERT INTO articles (title, content)
            VALUES (%s, %s)
            """
            cursor.execute(insert_article_query, (title, content))
            article_id = cursor.lastrowid

            if tags:
                select_existing_tags_query = 'SELECT id, name FROM tags WHERE name IN (%s)' % ','.join(['%s'] * len(tags))
                cursor.execute(select_existing_tags_query, tags)
                existing_tags = {row[1]: row[0] for row in cursor.fetchall()}

                new_tags = [tag for tag in tags if tag not in existing_tags]

                if new_tags:
                    insert_tags_query = 'INSERT INTO tags (name) VALUES (%s)'
                    cursor.executemany(insert_tags_query, [(tag,) for tag in new_tags])
                    cursor.execute(select_existing_tags_query, new_tags)
                    new_tag_ids = {row[1]: row[0] for row in cursor.fetchall()}
                    existing_tags.update(new_tag_ids)

                article_tag_relations = [(article_id, existing_tags[tag]) for tag in tags]

                insert_article_tag_query = 'INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)'
                cursor.executemany(insert_article_tag_query, article_tag_relations)

            connection.commit()

            return {'message': 'Статья и теги успешно добавлены!', 'article_id': article_id}

    except Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f'Ошибка при добавлении статьи: {e}')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
'''Функция для сохранения статьи в базу данных'''

def update_article_and_tags(id: int, title: str, contents: str, tags: list[str]) -> dict:
    try:
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor()

            connection.start_transaction()

            update_article_query = """
            UPDATE articles
            SET title = %s, contents = %s
            WHERE id = %s
            """
            
            cursor.execute(update_article_query, (title, contents, id))

            delete_article_tags_query = 'DELETE FROM article_tags WHERE article_id = %s'
            cursor.execute(delete_article_tags_query, (id,))

            select_existing_tags_query = 'SELECT id, name FROM tags WHERE name IN (%s)' % ','.join(['%s'] * len(tags))
            cursor.execute(select_existing_tags_query, tags)
            existing_tags = {row[1]: row[0] for row in cursor.fetchall()}

            new_tags = []
            article_tag_relations = []

            for tag in tags:
                if tag in existing_tags:
                    tag_id = existing_tags[tag]
                else:
                    new_tags.append(tag)

            if new_tags:
                insert_tags_query = 'INSERT INTO tags (name) VALUES (%s)'
                cursor.executemany(insert_tags_query, [(tag,) for tag in new_tags])

                cursor.execute(select_existing_tags_query, new_tags)
                new_tag_ids = {row[1]: row[0] for row in cursor.fetchall()}

                existing_tags.update(new_tag_ids)

            article_tag_relations = [(id, existing_tags[tag]) for tag in tags]

            insert_article_tag_query = 'INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)'
            cursor.executemany(insert_article_tag_query, article_tag_relations)

            connection.commit()

            return {'message': 'Статья и теги успешно обновлены!', 'article_id': id}

    except Error as e:
        connection.rollback()
        return HTTPException(status_code=500, detail=f'Ошибка: {e}')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
'''Функция для изменения статьи'''

def delete_article_from_db(article_id: int) -> dict:
    try:
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor()

            delete_article_query = 'DELETE FROM articles WHERE id = %s'
            cursor.execute(delete_article_query, (article_id,))

            if cursor.rowcount == 0:
                return {'message': 'Статья не найдена'}

            delete_article_tags_query = 'DELETE FROM article_tags WHERE article_id = %s'
            cursor.execute(delete_article_tags_query, (article_id,))

            connection.commit()

            return {'message': 'Статья успешно удалена'}

    except HTTPException as e:
        return {'message': f'Ошибка: {e}'}
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
'''Функция для удаления статьи из базы данных'''

def get_all_article_ids() -> list[int]:
    try:
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor()
            
            select_query = "SELECT id FROM articles"
            cursor.execute(select_query)
            
            result = cursor.fetchall()

            article_ids = [row[0] for row in result]
            return article_ids

    except Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
'''Функция для извлечения из базы данных всех id статей''' 
            
def get_article_by_id(article_id: int) -> dict:
    try:
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            select_article_query = """
            SELECT id, title, content, created_at, updated_at 
            FROM articles 
            WHERE id = %s
            """
            cursor.execute(select_article_query, (article_id,))
            article = cursor.fetchone()
            
            if article:
                return article
            else:
                return {'message': 'Статья не найдена'}

    except Error as e:
        return {'error': str(e)}
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
'''Функция для получения статьи по ID'''