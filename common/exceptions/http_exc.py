from fastapi import HTTPException, status


class EntityNotFoundError(HTTPException):
    def __init__(self, detail: str):
        self._detail = detail
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class BadRequestError(HTTPException):
    def __init__(self, detail: str):
        self._detail = detail
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

    def __str__(self):
        return self._detail


class AlreadyExistsError(HTTPException):
    def __init__(self, detail: str):
        self._detail = detail
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)

