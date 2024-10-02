class FailedToConnectError(ConnectionError):
    def __init__(self, detail: str):
        self._detail = detail

    def __str__(self) -> str:
        return f"Failed to connect: {self._detail}"


class DBError(Exception):
    def __init__(self, detail: str):
        self._detail = detail

    def __str__(self) -> str:
        return f"DB Error: something went wrong: {self._detail}"


class NotFoundError(Exception):
    def __init__(self, entity: str):
        self._entity = entity

    def __str__(self) -> str:
        return f"{self._entity} wasn't found"


