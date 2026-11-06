
from database.db_connection import get_connection
from psycopg.rows import dict_row


def execute_query(query: str, params: tuple = ()):
    

    with get_connection() as conn:

        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute("SET TRANSACTION READ ONLY")

            cur.execute(query, params) #we used to params to keep the query safe from SQL injection 

            results = cur.fetchall()

            return results
