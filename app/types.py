from typing import Annotated

from fastapi import Query

Limit = Annotated[int, Query(ge=1, le=100)]
Offset = Annotated[int, Query(ge=0, le=10000)]
Search = Annotated[str | None, Query(min_length=1, max_length=100)]
Year = Annotated[int | None, Query(ge=1900, le=2100)]
Month = Annotated[int | None, Query(ge=1, le=12)]
