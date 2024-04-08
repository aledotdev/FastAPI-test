from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class BaseObjectResponse(BaseModel, Generic[DataT]):
    data: DataT | None = None
    error: str | None = None


class BaseObjectListResponse(BaseModel, Generic[DataT]):
    data: list[DataT] | None = None
    error: str | None = None
