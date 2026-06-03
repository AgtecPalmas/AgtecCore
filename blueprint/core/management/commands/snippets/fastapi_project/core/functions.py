import uuid

from core.exceptions import UUIDValueException


def valid_uuid(id: str) -> uuid.UUID:
    try:
        return uuid.UUID(id)
    except ValueError as e:
        raise UUIDValueException() from e
