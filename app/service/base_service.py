"""
base service
"""

from typing import Any, Generic, Optional, Type, TypeVar

from pydantic import BaseModel

from app.db.unit_of_work import AsyncUnitOfWork
from app.repository.base_repository import BaseRepository

# Type variables for models and schemas
ModelType = TypeVar("ModelType")  # SQLAlchemy model
CreateSchemaType = TypeVar(
    "CreateSchemaType", bound=BaseModel
)  # Pydantic schema for create
UpdateSchemaType = TypeVar(
    "UpdateSchemaType", bound=BaseModel
)  # Pydantic schema for update
OutputSchemaType = TypeVar(
    "OutputSchemaType", bound=BaseModel
)  # Pydantic schema for output


class BaseService(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, OutputSchemaType]
):
    repository: Type[BaseRepository[ModelType]]
    output_schema: Type[OutputSchemaType]

    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow
        self.repository_instance = self.repository()
        # self.output_schema = output_schema

    async def prepare_create_data(self, create_data: CreateSchemaType) -> dict:
        """Hook for preparing creation data."""
        return create_data.model_dump()

    async def prepare_update_data(
        self, update_data: UpdateSchemaType, obj: ModelType
    ) -> dict:
        """
        Hook for preparing update data.
        Subclasses can override to customize behavior.
        """
        data = update_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(obj, field, value)
        return obj

    async def pre_create_hook(self, *args, **kwargs):
        """Pre-create hook for additional logic."""
        pass

    async def pre_update_hook(self, obj: ModelType, update_data: UpdateSchemaType):
        """Pre-update hook for additional logic."""
        pass

    async def post_create_hook(self, obj: ModelType):
        """Post-create hook for additional logic."""
        pass

    async def post_update_hook(self, obj: ModelType):
        """Post-update hook for additional logic."""
        pass

    async def create(self, create_data: CreateSchemaType) -> OutputSchemaType:
        """Main create method, wrapped with hooks and middleware logic."""
        async with self.uow() as session:
            await self.pre_create_hook(create_data=create_data)
            prepared_data = await self.prepare_create_data(create_data)
            obj = await self.repository_instance.create(session, prepared_data)
            await self.post_create_hook(obj)
            return self.output_schema.model_validate(obj)

    async def update(
        self, update_data: UpdateSchemaType, **primary_key_values: Any
    ) -> Optional[OutputSchemaType]:
        """
        Main update method, wrapped with hooks and middleware logic.
        """
        async with self.uow() as session:
            # Retrieve the existing object
            obj = await self.repository_instance.get_by_keys(session, primary_key_values)
            if not obj:
                return None

            # Pre-update logic
            await self.pre_update_hook(obj, update_data)

            # Prepare update data
            updated_obj = await self.prepare_update_data(update_data, obj)

            # Update the object in the repository
            obj = await self.repository_instance.update(session, updated_obj)

            # Post-update logic
            await self.post_update_hook(obj)

            # Return the updated object
            return self.output_schema.model_validate(obj)
