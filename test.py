import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

new_post = {
    'title': 'Machine Learning. How?',
    'content': 'Прежде чем начинать что-то делать, нужно понять, что ты собираешься делать.',
    'tags': ['#Python', '#ML-инженер', '#Карьера', '#IT']
}

def delete_article(id):
    try:

        
        r = requests.delete(f'http://localhost:8000/api/article/{id}')
        
        r.raise_for_status()

        print("Успешный запрос:")
        print(r.json())

    except HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except ConnectionError as conn_err:
        print(f"Ошибка соединения: {conn_err}")
    except Timeout as timeout_err:
        print(f"Ошибка тайм-аута: {timeout_err}")
    except RequestException as req_err:
        print(f"Произошла ошибка при выполнении запроса: {req_err}")
    except Exception as err:
        print(f"Произошла непредвиденная ошибка: {err}")

def create_article():
    try:
        r = requests.post(f'http://localhost:8000/api/article/', json=new_post)
        
        r.raise_for_status()

        print("Успешный запрос:")
        print(r.json())

    except HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except ConnectionError as conn_err:
        print(f"Ошибка соединения: {conn_err}")
    except Timeout as timeout_err:
        print(f"Ошибка тайм-аута: {timeout_err}")
    except RequestException as req_err:
        print(f"Произошла ошибка при выполнении запроса: {req_err}")
    except Exception as err:
        print(f"Произошла непредвиденная ошибка: {err}")


if __name__ == '__main__':
    create_article()