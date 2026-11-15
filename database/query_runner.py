from database.db_connection import (
    open_pool,
    close_pool,
    connection_pool
)

from database.query_executer import execute_query

from database.exceptions import DatabaseQueryTimeoutError, DatabasePoolTimeoutError, DatabaseConnectionError, DatabaseQueryError



def main():

    try:
        open_pool()

        print("Initial statistics:")
        print(connection_pool.get_stats())

        query = "SELECT pg_sleep(10);"

        results = execute_query(query)

        print("Query completed:", results)

    except DatabaseQueryTimeoutError as exc:
        print(f"Query Timeout: {exc}")

    except DatabasePoolTimeoutError as exc:
        print(f"Pool Error: {exc}")

    except DatabaseConnectionError as exc:
        print(f"Connection Error: {exc}")

    except DatabaseQueryError as exc:
        print(f"Database Error: {exc}")

    finally:
        close_pool()
        print("\nConnection pool closed!")


if __name__ == "__main__":
    main()