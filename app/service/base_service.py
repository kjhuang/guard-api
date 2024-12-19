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
        # self.repository_instance = self.repository(self.uow.session)
        # print("[BaseService]__init__, self.uow.session=", self.uow.session)
        # self.output_schema = output_schema

    async def prepare_create_data(self, create_data: CreateSchemaType) -> ModelType:
        """Hook for preparing creation data."""
        return ModelType(**create_data.model_dump())

    # async def prepare_update_data(
    #     self, update_data: UpdateSchemaType, obj: ModelType
    # ) -> dict:
    #     """
    #     Hook for preparing update data.
    #     Subclasses can override to customize behavior.
    #     """
    #     data = update_data.model_dump(exclude_unset=True)
    #     for field, value in data.items():
    #         setattr(obj, field, value)
    #     return obj

    async def pre_create_hook(self, *args, **kwargs):
        """Pre-create hook for additional logic."""
        pass

    async def pre_update_hook(self, update_data: UpdateSchemaType, **kwargs: Any):
        """Pre-update hook for additional logic."""
        pass

    async def post_create_hook(self, obj: ModelType):
        """Post-create hook for additional logic."""
        pass

    async def post_update_hook(self, obj: ModelType, **kwargs: Any):
        """Post-update hook for additional logic."""
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
            # updated_obj = await self.prepare_update_data(update_data, obj)

            # Update the object in the repository
            obj = await repository_instance.update(
                update_data.model_dump(), **primary_key_values
            )

            # Post-update logic
            # await self.post_update_hook(obj, **primary_key_values)

            # Return the updated object
            return self.output_schema.model_validate(obj)
