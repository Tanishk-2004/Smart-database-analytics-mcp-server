import pytest

from database.db_connection import open_pool, close_pool
from database.query_executer import execute_query
from database.exceptions import DatabaseQueryTimeoutError
from database.exceptions import DatabaseReadOnlyViolationError
from database.exceptions import DatabaseQueryError


@pytest.fixture(scope="session") 
def database_pool():
    open_pool()  #Initial setup---Before starting test///Pytest will take care automatically 

    yield       # Test executes here 

    close_pool()  #Cleaup-AFter test executes 


def test_execute_query_returns_results(database_pool):
    query = "SELECT 1 AS result;"

    results = execute_query(query)

    assert results == [{"result": 1}]





def test_execute_query_timeout(database_pool):
    query = "SELECT pg_sleep(10);"

    with pytest.raises(DatabaseQueryTimeoutError):
        execute_query(query)

def test_execute_query_read_only_violation(database_pool):
    query = "DELETE FROM customers WHERE customer_id = -999999999;"

    with pytest.raises(DatabaseReadOnlyViolationError):
        execute_query(query)

def test_execute_query_database_error(database_pool):
    query = "SELECT * FROM nonexistent_table;"

    with pytest.raises(DatabaseQueryError):
        execute_query(query)
