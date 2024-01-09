from typing import Optional

from fastapi import HTTPException


class GenericException(HTTPException):
    def __init__(self, error: Optional[str] = None):
        self.status_code = 400
        if error is None:
            error = "Error"
        self.detail = error


class CustomNotFoundException(GenericException):
    def __init__(self, error: Optional[str] = None):
        super().__init__(error or "Not found")
        self.status_code = 404


class CustomUUIDValueException(GenericException):
    def __init__(self, error: Optional[str] = None):
        super().__init__(error or "Invalid UUID value")
        self.status_code = 400
