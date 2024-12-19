"""
base repository
"""

from typing import Any, Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, Load
from sqlalchemy.sql import Select

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    # async def get(self, pk: Any) -> ModelType | None:
    #     """
    #     Get a single record by primary key.
    #     Supports any type of primary key.
    #     """
    #     return await self.session.get(self.model, pk)

    async def get_by_keys(
        self, load_options: Load | None = None, **primary_key_values: Any
    ) -> ModelType | None:
        """
        Get a single record by compound primary keys.
        :param primary_key_values: Key-value pairs representing the primary keys.
        """
        query: Select = select(self.model)
        # Apply loading strategy if provided
        if load_options:
            query = query.options(load_options)
        # Filter by primary key fields
        query = query.filter_by(**primary_key_values)

        # Execute the query
        result = await self.session.execute(query)

        return result.scalars().first()

        # stmt = select(self.model).filter_by(**primary_key_values)
        # result = await self.session.execute(stmt)
        # return result.scalar_one_or_none()

    async def get_dynamic(self, **kwargs: Any) -> ModelType | None:
        """
        Get a record dynamically based on primary key(s).
        Automatically retrieves the primary key column(s) from the model.
        """
        primary_keys = self.model.__mapper__.primary_key  # SQLAlchemy introspection
        if not set(kwargs.keys()) == {key.name for key in primary_keys}:
            raise ValueError("Provided keys do not match model's primary keys")

        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        """
        Get all records for the model.
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj: ModelType):
        """
        Add a new record to the session.
        """
        self.session.add(obj)
        await self.session.flush()

    async def update(
        self, update_data: dict, **primary_key_values: Any
    ) -> ModelType | None:
        """
        Update a record by primary keys.
        :param primary_key_values: Key-value pairs representing the primary keys.
        :param update_data: A dictionary of fields to update.
        :return: The updated model instance or None if not found.
        """
        obj = await self.get_by_keys(**primary_key_values)
        if not obj:
            return None

        # Update fields dynamically
        for field, value in update_data.items():
            if hasattr(obj, field):
                print(f"update '{field}' with '{value}'")
                setattr(obj, field, value)

        return obj  # Changes will be persisted when session.commit() is called

    async def delete(self, **primary_key_values: Any) -> None:
        """
        Delete a record by primary keys.
        :param primary_key_values: Key-value pairs representing the primary keys.
        """
        obj = await self.get_by_keys(**primary_key_values)
        if obj:
            await self.session.delete(obj)

    async def delete_obj(self, obj: ModelType):
        """
        Remove a record from the session.
        """
        await self.session.delete(obj)
