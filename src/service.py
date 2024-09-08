from fastapi import HTTPException
from datetime import datetime
from typing import List

from src.utils import get_db_connection
from mysql.connector import Error

# Функция для сохранения статьи в базу данных
def add_article_with_tags(title: str, content: str, tags: list[str]) -> dict:
    try:
        # Установить соединение с базой данных
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor()

            # Начало транзакции
            connection.start_transaction()

            # 1. Вставка новой статьи с указанием времени создания
            insert_article_query = """
            INSERT INTO articles (title, content, created_at)
            VALUES (%s, %s, %s)
            """

            created_at = datetime.now()
            cursor.execute(insert_article_query, (title, content, created_at))

            # Получение ID вставленной статьи
            article_id = cursor.lastrowid

            # 2. Загрузка всех существующих тегов одним запросом
            select_existing_tags_query = 'SELECT id, name FROM tags WHERE name IN (%s)' % ','.join(['%s'] * len(tags))
            cursor.execute(select_existing_tags_query, tags)
            existing_tags = {row[1]: row[0] for row in cursor.fetchall()}

            # Списки для новых тегов и их связей с статьей
            new_tags = []
            article_tag_relations = []

            for tag in tags:
                if tag in existing_tags:
                    # Тег уже существует
                    tag_id = existing_tags[tag]
                else:
                    # Добавление нового тега
                    new_tags.append(tag)

            if new_tags:
                # Вставляем новые теги пакетно
                insert_tags_query = 'INSERT INTO tags (name) VALUES (%s)'
                cursor.executemany(insert_tags_query, [(tag,) for tag in new_tags])

                # Получаем ID добавленных тегов
                cursor.execute(select_existing_tags_query, new_tags)
                new_tag_ids = {row[1]: row[0] for row in cursor.fetchall()}

                # Обновляем словарь существующих тегов новыми тегами
                existing_tags.update(new_tag_ids)

            # Формируем список связей статьи с тегами
            article_tag_relations = [(article_id, existing_tags[tag]) for tag in tags]

            # 3. Связываем статью с тегами пакетно
            insert_article_tag_query = 'INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)'
            cursor.executemany(insert_article_tag_query, article_tag_relations)

            # Фиксируем все изменения
            connection.commit()

            return {'message': 'Статья и теги успешно добавлены!', 'article_id': article_id}

    except Error as e:
        connection.rollback()  # Откатываем транзакцию в случае ошибки
        return HTTPException(status_code=500, detail=f'Ошибка: {e}')

    finally:    
        # Закрыть соединение
        if connection.is_connected():
            cursor.close()
            connection.close()

# Функция для изменения статьи
def update_article_and_tags(id: int, title: str, contents: str, tags: list[str]) -> dict:
    try:
        # Установить соединение с базой данных
        connection = get_db_connection()

        if connection.is_connected():
            cursor = connection.cursor()

            # Начало транзакции
            connection.start_transaction()

            # 1. Обновление статьи
            update_article_query = """
            UPDATE articles
            SET title = %s, contents = %s, updated_at = %s
            WHERE id = %s
            """
            
            created_at = datetime.now()
            cursor.execute(update_article_query, (title, contents, created_at, id))

            # 2. Работа с тегами
            # Удаляем старые связи статьи с тегами
            delete_article_tags_query = 'DELETE FROM article_tags WHERE article_id = %s'
            cursor.execute(delete_article_tags_query, (id,))

            # 3. Загрузка всех существующих тегов одним запросом
            select_existing_tags_query = 'SELECT id, name FROM tags WHERE name IN (%s)' % ','.join(['%s'] * len(tags))
            cursor.execute(select_existing_tags_query, tags)
            existing_tags = {row[1]: row[0] for row in cursor.fetchall()}

            # Списки для новых тегов и их связей с статьей
            new_tags = []
            article_tag_relations = []

            for tag in tags:
                if tag in existing_tags:
                    # Тег уже существует
                    tag_id = existing_tags[tag]
                else:
                    # Добавление нового тега
                    new_tags.append(tag)

            if new_tags:
                # Вставляем новые теги пакетно
                insert_tags_query = 'INSERT INTO tags (name) VALUES (%s)'
                cursor.executemany(insert_tags_query, [(tag,) for tag in new_tags])

                # Получаем ID добавленных тегов
                cursor.execute(select_existing_tags_query, new_tags)
                new_tag_ids = {row[1]: row[0] for row in cursor.fetchall()}

                # Обновляем словарь существующих тегов новыми тегами
                existing_tags.update(new_tag_ids)

            # Формируем список связей статьи с тегами
            article_tag_relations = [(id, existing_tags[tag]) for tag in tags]

            # Связываем статью с тегами пакетно
            insert_article_tag_query = 'INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)'
            cursor.executemany(insert_article_tag_query, article_tag_relations)

            # Фиксируем все изменения
            connection.commit()

            return {'message': 'Статья и теги успешно обновлены!', 'article_id': id}

    except Error as e:
        connection.rollback()  # Откатываем транзакцию в случае ошибки
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
        connection = get_db_connection()

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

    except HTTPException as e:
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
        connection = get_db_connection()

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
        connection = get_db_connection()

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