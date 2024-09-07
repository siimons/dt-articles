from fastapi import HTTPException
from datetime import datetime
from typing import List
from decouple import config 

from mysql.connector import Error
import mysql.connector

HOST = config('HOST')
DATABASE = config('DATABASE')
USER = config('USER')
PASSWORD = config('PASSWORD')

# Функция для сохранения статьи в базу данных
def add_article_with_tags(title: str, content: str, tags: list[str], updated_at: datetime) -> dict:
    try:
        # Установить соединение с базой данных
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,  
            user=USER,          
            password=PASSWORD        
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Получить текущее время
            # updated_at = datetime.now()

            # 1. Вставка новой статьи с указанием времени создания
            insert_article_query = """
            INSERT INTO articles (title, content, created_at)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_article_query, (title, content, updated_at))

            # Получение ID вставленной статьи
            article_id = cursor.lastrowid

            # 2. Работа с тегами
            for tag in tags:
                # Проверка, существует ли тег в базе данных
                select_tag_query = 'SELECT id FROM tags WHERE name = %s'
                cursor.execute(select_tag_query, (tag,))
                result = cursor.fetchone()

                if result:
                    # Тег уже существует, получаем его ID
                    tag_id = result[0]
                else:
                    # Если тега нет, вставляем новый тег
                    insert_tag_query = 'INSERT INTO tags (name) VALUES (%s)'
                    cursor.execute(insert_tag_query, (tag,))
                    tag_id = cursor.lastrowid

                # 3. Связь статьи с тегами через таблицу article_tags
                insert_article_tag_query = 'INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)'
                cursor.execute(insert_article_tag_query, (article_id, tag_id))

            # Фиксируем все изменения
            connection.commit()

            return {'message': 'Статья и теги успешно добавлены!', 'article_id': article_id}

    except Error as e:
        return HTTPException(status_code=500, detail=f'Ошибка: {e}')
        
    finally:
        # Закрыть соединение
        if connection.is_connected():
            cursor.close()
            connection.close()
            
# Функция для изменения статьи
def update_article_and_tags(id: int, title: str, contents: str, tags: list[str], updated_at: datetime) -> dict:
    try:
        # Установить соединение с базой данных
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Получить текущее время
            # updated_at = datetime.now()

            # 1. Обновление статьи
            update_article_query = """
            UPDATE articles
            SET title = %s, contents = %s, updated_at = %s
            WHERE id = %s
            """
            cursor.execute(update_article_query, (title, contents, updated_at, id))

            # 2. Работа с тегами
            # Удаляем старые связи статьи с тегами
            delete_article_tags_query = 'DELETE FROM article_tags WHERE article_id = %s'
            cursor.execute(delete_article_tags_query, (id,))

            # Добавляем новые связи статьи с тегами
            for tag in tags:
                # Проверка, существует ли тег в базе данных
                select_tag_query = 'SELECT id FROM tags WHERE name = %s'
                cursor.execute(select_tag_query, (tag,))
                result = cursor.fetchone()

                if result:
                    # Тег уже существует, получаем его ID
                    tag_id = result[0]
                else:
                    # Если тега нет, вставляем новый тег
                    insert_tag_query = 'INSERT INTO tags (name) VALUES (%s)'
                    cursor.execute(insert_tag_query, (tag,))
                    tag_id = cursor.lastrowid

                # Связь статьи с тегами через таблицу article_tags
                insert_article_tag_query = 'INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)'
                cursor.execute(insert_article_tag_query, (id, tag_id))

            # Фиксируем все изменения
            connection.commit()

            return {'message': 'Статья и теги успешно обновлены!', 'article_id': id}

    except Error as e:
        # В случае ошибки возвращаем HTTPException с кодом 500
        return HTTPException(status_code=500, detail=f'Ошибка: {e}')

    finally:
        # Закрыть соединение
        if connection.is_connected():
            cursor.close()
            connection.close()
            
# Функция для удаления статьи из базы данных
def delete_article_from_db(article_id: int) -> dict:
    try:
        # Установить соединение с базой данных
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Удаляем статью и связанные с ней теги
            delete_article_query = 'DELETE FROM articles WHERE id = %s'
            cursor.execute(delete_article_query, (article_id,))

            # Проверяем, была ли удалена хотя бы одна строка
            if cursor.rowcount == 0:
                return {'message': 'Статья не найдена'}

            # Удаляем связанные с статьей теги
            delete_article_tags_query = 'DELETE FROM article_tags WHERE article_id = %s'
            cursor.execute(delete_article_tags_query, (article_id,))

            # Фиксируем все изменения
            connection.commit()

            return {'message': 'Статья успешно удалена'}

    except Error as e:
        # Возвращаем сообщение об ошибке
        return {'message': f'Ошибка: {e}'}

    finally:
        # Закрыть соединение
        if connection.is_connected():
            cursor.close()
            connection.close()

# Функция для извлечения из базы данных всех id статей 
def get_all_article_ids() -> List[int]:
    try:
        # Установить соединение с базой данных
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # SQL-запрос для получения всех id статей
            select_query = "SELECT id FROM articles"
            cursor.execute(select_query)
            
            # Извлекаем все результаты запроса
            result = cursor.fetchall()

            # Возвращаем список id
            article_ids = [row[0] for row in result]
            return article_ids

    except Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return []

    finally:
        # Закрыть соединение
        if connection.is_connected():
            cursor.close()
            connection.close()
            
# Функция для получения статьи по ID
def get_article_by_id(article_id: int) -> dict:
    try:
        # Установить соединение с базой данных
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # SQL-запрос для получения статьи по ID
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
        # Закрыть соединение
        if connection.is_connected():
            cursor.close()
            connection.close()