from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.user import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(
            self,
            model: Type[ModelType]
    ):
        self.model = model

    async def get(
            self,
            session: AsyncSession,
            obj_id: int,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_open(
            self,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        open_projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            )
        )
        return open_projects.scalars().all()

    async def save_session(
            self,
            session: AsyncSession,
            created_object: ModelType,
            save_objects: list[ModelType],
    ) -> None:
        """
        Функция для сохранения измененных объектов
        во время инвестирования
        """
        session.add_all(save_objects)
        session.add(created_object)
        await session.commit()
        await session.refresh(created_object)

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            session: AsyncSession,
            obj_in: CreateSchemaType,
            change: bool = False,
            user: Optional[User] = None,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        obj_in_data['create_date'] = datetime.today()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        if not change:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            session: AsyncSession,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            session: AsyncSession,
            db_obj: ModelType,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
