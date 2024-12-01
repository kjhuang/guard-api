"""
convert model: sqlalchemy <-> pydantic
"""

from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def sqlalchemy_to_pydantic(instance, pydantic_model: Type[T]) -> T:
    """
    Convert a SQLAlchemy instance to a Pydantic model.
    """
    return pydantic_model.model_validate(instance)


def pydantic_to_sqlalchemy(pydantic_model: BaseModel, sqlalchemy_model: Type):
    """
    Convert a Pydantic model to a SQLAlchemy instance.
    """
    return sqlalchemy_model(**pydantic_model.model_dump())
