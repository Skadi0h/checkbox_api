from typing import TypeVar

from sqlmodel import SQLModel

ModelTypeT = TypeVar('ModelTypeT', bound=SQLModel)
