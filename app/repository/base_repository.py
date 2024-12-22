"""
base repository
"""

from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy.sql import Select, asc, desc

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class InvalidRelationError(Exception):
    pass


class InvalidColumnError(Exception):
    pass


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    def _apply_load_relations(self, query: Select, load_relations: Optional[List[str]]):
        """
        Apply relationship loading options to a query.
        """
        if load_relations:
            for relation in load_relations:
                if hasattr(self.model, relation):
                    query = query.options(joinedload(getattr(self.model, relation)))
                else:
                    raise InvalidRelationError(
                        f"'{self.model.__name__}' has no relationship '{relation}'"
                    )
        return query

    def _apply_load_relations2(
        self, query: Select, load_relations: Optional[List[str]]
    ) -> Select:
        """
        Apply relationship loading options to a query, supporting nested relations.
        Example:
            load_relations=["site", "site.owner", "comments.author"]
        """
        if not load_relations:
            return query

        for relation_path in load_relations:
            parts = relation_path.split(".")
            current_model = self.model
            current_loader = joinedload(getattr(current_model, parts[0], None))

            if not hasattr(current_model, parts[0]):
                raise InvalidRelationError(
                    f"'{current_model.__name__}' has no relationship '{parts[0]}'"
                )

            for part in parts[1:]:
                current_model = getattr(current_model, part, None)
                if current_model is None:
                    raise InvalidRelationError(
                        f"'{current_model.__name__}' has no relationship '{part}'"
                    )
                current_loader = current_loader.joinedload(part)

            query = query.options(current_loader)

        return query

    def _apply_filters(
        self, query: Select, filters: Optional[Dict[Tuple[str, str], Any]]
    ):
        """
        Apply dynamic filters to a query.
        Supports operators like '=', '>=', '<=', 'IN', etc.
        """
        if filters:
            for (field, operator), value in filters.items():
                if not hasattr(self.model, field):
                    raise InvalidColumnError(
                        f"'{self.model.__name__}' has no column '{field}'"
                    )
                column = getattr(self.model, field)

                if operator == "=":
                    query = query.where(column == value)
                elif operator == "!=":
                    query = query.where(column != value)
                elif operator == ">":
                    query = query.where(column > value)
                elif operator == "<":
                    query = query.where(column < value)
                elif operator == ">=":
                    query = query.where(column >= value)
                elif operator == "<=":
                    query = query.where(column <= value)
                elif operator == "IN" or operator == "in":
                    query = query.where(column.in_(value))
                elif operator == "NOT IN" or operator == "not in":
                    query = query.where(~column.in_(value))
                else:
                    raise ValueError(f"Unsupported operator: {operator}")
        return query

    def _apply_pagination(
        self, query: Select, limit: Optional[int], offset: Optional[int]
    ) -> Select:
        """
        Apply pagination to a query.
        """
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query

    def _apply_sorting(
        self, query: Select, order_by: Optional[Dict[str, str]] = None
    ) -> Select:
        """
        Apply multi-column sorting to a query.
        Example:
            order_by={"name": "asc", "date": "desc"}
        """
        if order_by:
            for column_name, direction in order_by.items():
                if not hasattr(self.model, column_name):
                    raise InvalidColumnError(
                        f"'{self.model.__name__}' has no column '{column_name}'"
                    )
                column = getattr(self.model, column_name)
                if direction == "asc":
                    query = query.order_by(asc(column))
                elif direction == "desc":
                    query = query.order_by(desc(column))
                else:
                    raise ValueError(f"Invalid sorting direction: {direction}")
        return query

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

    async def get_by_keys(
        self, load_relations: Optional[List[str]] = None, **primary_key_values: Any
    ) -> Optional[ModelType]:
        """
        Fetch a single object by primary key(s) with optional relationship loading.
        """
        query = select(self.model)
        query = self._apply_load_relations(query, load_relations)

        # Apply primary key filters
        for key, value in primary_key_values.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
            else:
                raise InvalidColumnError(
                    f"'{self.model.__name__}' has no column '{key}'"
                )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def query(
        self,
        load_relations: Optional[List[str]] = None,
        filters: Optional[Dict[Tuple[str, str], Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Dict[str, str]] = None,
    ) -> List[ModelType]:
        """
        Perform a dynamic query with optional relationship loading and filters.
        """
        query = select(self.model)
        query = self._apply_load_relations(query, load_relations)
        query = self._apply_filters(query, filters)
        query = self._apply_pagination(query, limit, offset)
        query = self._apply_sorting(query, order_by)

        result = await self.session.execute(query)
        return result.scalars().all()
