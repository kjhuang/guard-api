"""
base service
"""

from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel

from app.db.unit_of_work import AsyncUnitOfWork
from app.repository.base_repository import BaseRepository

# Type variables for models and schemas
# SQLAlchemy model
ModelType = TypeVar("ModelType")
# Pydantic schema for create
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# Pydantic schema for update
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# Pydantic schema for output
OutputSchemaType = TypeVar("OutputSchemaType", bound=BaseModel)
# pydantic schema for query
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class BaseService(
    Generic[
        ModelType, CreateSchemaType, UpdateSchemaType, OutputSchemaType, QuerySchemaType
    ]
):
    repository: Type[BaseRepository[ModelType]]
    output_schema: Type[OutputSchemaType]
    query_schema: Type[QuerySchemaType]
    relation_strategies: Dict[str, List[str]] = {"basic": [], "full": []}

    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    def _get_relation_strategy(self, strategy: str) -> List[str]:
        """
        Map a relation strategy name to actual relation keys.
        """
        return self.relation_strategies.get(strategy, [])

    async def prepare_create_data(self, create_data: CreateSchemaType) -> ModelType:
        """Hook for preparing creation data."""
        return ModelType(**create_data.model_dump())

    async def prepare_update_data(
        self, update_data: UpdateSchemaType, obj: ModelType
    ) -> dict:
        """
        Hook for preparing update data.
        """
        data = update_data.model_dump(exclude_unset=True)
        # for field, value in data.items():
        #     setattr(obj, field, value)
        return data

    async def pre_create_hook(self, *args, **kwargs):
        """Pre-create hook for additional logic."""
        pass

    async def pre_update_hook(self, update_data: UpdateSchemaType, **kwargs: Any):
        """Pre-update hook for additional logic."""
        pass

    async def pre_delete_hook(self, obj: ModelType):
        """Pre-delete hook for additional logic."""
        pass

    async def post_create_hook(self, obj: ModelType):
        """Post-create hook for additional logic."""
        pass

    async def post_update_hook(self, obj: ModelType, **kwargs: Any):
        """Post-update hook for additional logic."""
        pass

    async def post_delete_hook(self, obj: ModelType):
        """Post-delete hook for additional logic."""
        pass

    async def create(self, create_data: CreateSchemaType) -> OutputSchemaType:
        """Main create method, wrapped with hooks and middleware logic."""
        async with self.uow as uow:
            # await self.pre_create_hook(create_data=create_data)
            prepared_data = await self.prepare_create_data(create_data)

            repository_instance = self.repository(uow.session)
            await repository_instance.create(prepared_data)
            # await self.post_create_hook(prepared_data)
            return self.output_schema.model_validate(prepared_data)

    async def update(
        self, update_data: UpdateSchemaType, **primary_key_values: Any
    ) -> Optional[OutputSchemaType]:
        """
        Main update method, wrapped with hooks and middleware logic.
        """
        async with self.uow as uow:
            repository_instance = self.repository(uow.session)
            # Retrieve the existing object
            obj = await repository_instance.get_by_keys(**primary_key_values)
            if not obj:
                return None

            # Pre-update logic
            # await self.pre_update_hook(update_data, **primary_key_values)

            # Prepare update data
            updated_obj = await self.prepare_update_data(update_data, obj)

            # Update the object in the repository
            obj = await repository_instance.update(updated_obj, **primary_key_values)

            # Post-update logic
            # await self.post_update_hook(obj, **primary_key_values)

            # Return the updated object
            return self.output_schema.model_validate(obj)

    async def delete_by_keys(self, **primary_key_values: Any) -> bool:
        async with self.uow as uow:
            repository_instance = self.repository(uow.session)
            obj = await repository_instance.get_by_keys(**primary_key_values)
            if not obj:
                return False

            await self.pre_delete_hook(obj)
            await repository_instance.delete_obj(obj)
            await self.post_delete_hook(obj)
            return True

    async def get_by_keys(
        self, relation_strategy: str = "basic", **primary_key_values: Any
    ) -> Optional[QuerySchemaType]:
        """
        Get an entity by primary keys with a predefined relation strategy.
        """
        async with self.uow as uow:
            relations = self._get_relation_strategy(relation_strategy)
            repository_instance = self.repository(uow.session)
            obj = await repository_instance.get_by_keys(
                load_relations=relations, **primary_key_values
            )
            if obj:
                return self.query_schema.model_validate(obj)
            return None

    async def query(
        self,
        filters: Optional[Dict[Tuple[str, str], Any]] = None,
        relation_strategy: str = "basic",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[Dict[str, str]] = None,
    ) -> List[QuerySchemaType]:
        """
        Query entities with filters, sorting, pagination, and predefined relation strategy.
        """
        async with self.uow as uow:
            relations = self._get_relation_strategy(relation_strategy)
            repository_instance = self.repository(uow.session)
            objs = await repository_instance.query(
                filters=filters,
                load_relations=relations,
                limit=limit,
                offset=offset,
                order_by=order_by,
            )
            return [self.query_schema.model_validate(obj) for obj in objs]
