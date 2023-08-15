from typing import List, Union

from pydantic import BaseModel


class PaginationBase(BaseModel):
    count: int = 0
    next: Union[str, None] = None
    previous: Union[str, None] = None
    results: List[dict] = None