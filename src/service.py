from fastapi import HTTPException
from datetime import datetime
from decouple import config 

from mysql.connector import Error
import mysql.connector

HOST = config('HOST')
DATABASE = config('DATABASE')
USER = config('USER')
PASSWORD = config('PASSWORD')

def add_article_with_tags(title: str, content: str, tags: list[str]) -> dict:
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
            created_at = datetime.now()

            # 1. Вставка новой статьи с указанием времени создания
            insert_article_query = """
            INSERT INTO articles (title, content, created_at)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_article_query, (title, content, created_at))

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