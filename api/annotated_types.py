from typing import Annotated, Literal

from fastapi import Path, Query

SortByQuery = Annotated[
    Literal["asc", "desc",],
    Query(alias="sortBy")
]

PageQuery = Annotated[
    int,
    Query(ge=1, alias="page")
]

PageNumberQuery = Annotated[
    int,
    Query(ge=1, alias="pageNumber")
]

CategoryID = Annotated[
    int,
    Path(
        alias="id",
        title="Category ID",
        description="Category unique identifier",
        examples=[42]
    )
]

CategorySortAttrQuery = Annotated[
    Literal["id", "name"],
    Query(alias="sort")
]
