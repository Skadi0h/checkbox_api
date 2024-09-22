from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.v1.generics import GenericModel
from sqlmodel.sql._expression_select_cls import SelectOfScalar, Select

T = TypeVar('T')


class PageParams(BaseModel):
    page: int = Field(gt=1)
    size: int = Field(gt=1, default=10)


class PagedModelResponse(GenericModel, Generic[T]):
    total: int
    page: int
    size: int
    results: list[T]


async def paginate_query(
        *,
        page_params: PageParams,
        query: Select | SelectOfScalar,
) -> Select | SelectOfScalar:
    return query.offset((page_params.page - 1) * page_params.size).limit(page_params.size)
