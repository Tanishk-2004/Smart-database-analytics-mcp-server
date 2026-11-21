from psycopg.errors import QueryCanceled,ReadOnlySqlTransaction
from psycopg import OperationalError
from psycopg_pool import PoolTimeout
from psycopg.rows import dict_row

from database.db_connection import connection_pool

from database.exceptions import DatabaseQueryTimeoutError, DatabasePoolTimeoutError, DatabaseConnectionError,DatabaseQueryError,DatabaseReadOnlyViolationError



def execute_query(query: str, params: tuple = ()):

    try:
        with connection_pool.connection() as conn:

            with conn.cursor(row_factory=dict_row) as cur:

                cur.execute("SET TRANSACTION READ ONLY")

                cur.execute(
                    "SET LOCAL statement_timeout = '5000ms'"
                )

                cur.execute(query, params)

                results = cur.fetchall()

                return results

    except QueryCanceled as exc:
        raise DatabaseQueryTimeoutError(
            "The database query exceeded the allowed execution time."
        ) from exc

    except PoolTimeout as exc:
        raise DatabasePoolTimeoutError(
            "Unable to acquire a database connection. Please try again."
        ) from exc

    except OperationalError as exc:
        raise DatabaseConnectionError(
            "Unable to communicate with the database."
        ) from exc

    except ReadOnlySqlTransaction as exc:
        raise DatabaseReadOnlyViolationError(
            "This operation is not allowed. The database is read-only."
        ) from exc

    except Exception as exc:
        # Handle only PostgreSQL errors here.
        from psycopg import Error

        if isinstance(exc, Error):
            raise DatabaseQueryError(
                "An error occurred while executing the database query."
            ) from exc

        raise