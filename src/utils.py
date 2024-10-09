from decouple import config
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
import mysql.connector

HOST = config('HOST')
PORT = config("PORT")
DATABASE = config('MYSQL_DATABASE')
USER = config('MYSQL_USER')
PASSWORD = config('MYSQL_PASSWORD')

def get_db_connection() -> PooledMySQLConnection | MySQLConnectionAbstract:
    return mysql.connector.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,  
        user=USER,          
        password=PASSWORD
    )
