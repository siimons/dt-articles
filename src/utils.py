from decouple import config
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
import mysql.connector

HOST = config('HOST')
DATABASE = config('DATABASE')
USER = config('USER')
PASSWORD = config('PASSWORD')

def get_db_connection() -> PooledMySQLConnection | MySQLConnectionAbstract:
    return mysql.connector.connect(
        host=HOST,
        database=DATABASE,  
        user=USER,          
        password=PASSWORD        
    )
