from typing import List, Optional, Union

from pydantic import BaseModel


class PaginationBase(BaseModel):
    count: int = 0
    next: Union[str, None] = None
    previous: Union[str, None] = None
    results: Optional[List[dict]] = None
