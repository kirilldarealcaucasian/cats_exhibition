from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from common.exceptions import DBError, NotFoundError
from internal.orm_models.breed import Breed
from internal.orm_models.kitten import Kitten
from internal.storage import db_client

from .sqlalchemy_repo import SqlAlchemyRepo


class KittenRepo(SqlAlchemyRepo):
    def __init__(self):
        super().__init__(model=Kitten)

    async def get_kittens_by_breed(
        self, breed_name: str
    ) -> list[Kitten]:
        stmt = (
            select(Kitten, Breed)
            .join(Breed, Kitten.breed_id == Breed.id)
            .where(Breed.name == breed_name)
        ).options(
            joinedload(Kitten.breed)
        )
        async with db_client.session as session:
            kittens = (await session.scalars(stmt)).all()
            return list(kittens)

    async def get_all_kittens(self):
        stmt = select(self._orm_model).options(
            joinedload(Kitten.breed)
        )
        async with db_client.session as session:
            try:
                res = (await session.scalars(stmt)).all()
            except SQLAlchemyError as e:
                raise DBError(detail=str(e))
            return list(res)

    async def get_kitten_by_id(self, id: int) -> Kitten:
        stmt = select(Kitten).where(Kitten.id == id).options(
            joinedload(Kitten.breed)
        )

        async with db_client.session as session:
            kitten = (await session.execute(stmt)).scalar_one_or_none()
            if not kitten:
                raise NotFoundError(entity="Kitten")

            return kitten
