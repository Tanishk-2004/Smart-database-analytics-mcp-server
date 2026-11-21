class DatabaseQueryTimeoutError(Exception):
    pass


class DatabasePoolTimeoutError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


class DatabaseQueryError(Exception):
    pass

class DatabaseReadOnlyViolationError(Exception):
    pass