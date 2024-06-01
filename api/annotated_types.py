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
    Literal["id", "name", "slug"],
    Query(alias="sort")
]


BookPrivateSortAttrQuery = Annotated[
    Literal["id", "name", "slug", "title", "author", "tags"],
    Query(alias="sort")
]

BookPrivateID = Annotated[
    int,
    Path(
        alias="id",
        title="BookPrivate ID",
        description="BookPrivate unique identifier",
        examples=[42]
    )
]

GeneralBookSortAttrQuery = Annotated[
    Literal["id", "name", "slug", "title", "author", "tags"],
    Query(alias="sort")
]

GeneralBookID = Annotated[
    int,
    Path(
        alias="id",
        title="GeneralBook ID",
        description="GeneralBook unique identifier",
        examples=[42]
    )
]

UsersSortAttrQuery = Annotated[
    Literal["id", "email",],
    Query(alias="sort")
]