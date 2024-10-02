from fastapi import Depends

from common.exceptions import AlreadyExistsError, BadRequestError, DBError
from common.logger import logger
from internal.repositories import BreedRepo
from internal.schemas import BreedID, CreateBreedS, ReturnBreedS


class BreedService:
    def __init__(self, breed_repo: BreedRepo = Depends()):
        self._breed_repo: BreedRepo = breed_repo

    async def get_breeds(self) -> list[ReturnBreedS]:
        try:
            breeds = await self._breed_repo.get_all()
            return [
                ReturnBreedS(
                    instance_id=breed.id,
                    name=breed.name
                ) for breed in breeds
            ]
        except DBError as e:
            logger.error(
                msg="failed to get breeds",
                exc_info=str(e),
            )
            raise e

    async def create(self, create_dto: CreateBreedS) -> BreedID:
        create_data: dict = create_dto.model_dump(
            exclude_none=True, exclude_unset=True
        )
        if not create_data:
            raise BadRequestError(
                detail="Invalid creation data"
            )
        try:
            instance_id: int = await self._breed_repo.create(
                data=create_data
            )
            return BreedID(
                instance_id=instance_id
            )
        except (Exception, DBError) as e:
            logger.error(msg="failed to create breed", exc_info=str(e))
            raise AlreadyExistsError(
                detail="Breed already exists"
            )