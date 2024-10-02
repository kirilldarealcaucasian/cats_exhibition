from sqlalchemy import select
from typing_extensions import Union

from common.exceptions import NotFoundError
from internal.orm_models.breed import Breed

from ..storage import db_client
from .sqlalchemy_repo import SqlAlchemyRepo


class BreedRepo(SqlAlchemyRepo):
    def __init__(self):
        super().__init__(model=Breed)

    async def get_breed_by_name(
        self, name: str
    ) -> Breed:
        async with db_client.session as session:
            stmt = select(Breed).where(Breed.name == name)

            breed: Union[Breed, None] = (
                await session.execute(stmt)
            ).scalar_one_or_none()

            if not breed:
                raise NotFoundError(entity="Breed")
            return breed
