
import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()


connection_pool = ConnectionPool(
    conninfo="",
    kwargs={
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "connect_timeout": 10,  # If postgre does not respond within 10 secs it aborts and throws an error 
    },
    min_size=0,
    max_size=5,
    timeout=10, # waiting time for new  connection requests if all the 5 connections are busy
    max_idle=600,
    max_lifetime=3600,
    open=False,
)


def open_pool():
    connection_pool.open()


def close_pool():
    connection_pool.close()
