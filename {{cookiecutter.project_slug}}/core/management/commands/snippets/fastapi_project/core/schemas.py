from pydantic import BaseModel


class PaginationBase(BaseModel):
    count: int = 0
    next: str | None = None
    previous: str | None = None
    results: list[dict] | None = None
