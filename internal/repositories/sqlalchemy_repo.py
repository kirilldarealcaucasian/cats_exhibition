from typing import Generic, Type, TypeVar

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions import DBError, ModelConversionError, NotFoundError
from internal.orm_models import Breed, Kitten
from internal.storage import db_client

__all__ = "SqlAlchemyRepo"


ModelDataT = TypeVar("ModelDataT", Kitten, Breed)


class SqlAlchemyRepo(Generic[ModelDataT]):
    def __init__(self, model: Type[ModelDataT]):
        self._orm_model = model

    async def get_all(self) -> list[ModelDataT]:
        async with db_client.session as session:
            stmt = select(self._orm_model)
            try:
                res = (await session.scalars(stmt)).all()
            except SQLAlchemyError as e:
                raise DBError(
                    detail=str(e)
                )
            return list(res)

    async def __get_by_id(self, id: int) -> ModelDataT:
        async with db_client.session as session:
            stmt = select(self._orm_model).where(self._orm_model.id == id)
            res = (await session.execute(stmt)).scalar_one_or_none()
            if res is None:
                raise NotFoundError(entity="Kitten")
            return res

    async def create(self, data: dict) -> int:
        async with db_client.session as session:
            try:
                model = self._orm_model(**data)
            except Exception as e:
                raise ModelConversionError(detail=str(e))

            session.add(model)
            await self.commit(session=session)
            return model.id

    async def update(self, instance_id: int, data: dict) -> ModelDataT:
        stmt = update(self._orm_model).where(
            self._orm_model.id == instance_id
        ).values(**data)

        async with db_client.session as session:
            _ = await session.execute(stmt)
            await self.commit(session=session)
            session.expire_all()

            select_stmt = select(self._orm_model).where(
                self._orm_model.id == instance_id
            )
            return (await session.execute(select_stmt)).scalar_one_or_none()

    async def delete(self, id: int) -> None:
        obj = await self.__get_by_id(
            id=id
        )  # raises exc if obj doesn't exist

        async with db_client.session as session:
            await session.delete(obj)
            await self.commit(session=session)

    async def commit(self, session: AsyncSession):
        try:
            await session.commit()
        except SQLAlchemyError as e:
            raise DBError(detail=str(e))
