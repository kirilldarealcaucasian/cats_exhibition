from typing import TypeAlias

from fastapi import Depends

from common.exceptions import (
    BadRequestError,
    DBError,
    EntityNotFoundError,
    NotFoundError,
)
from common.logger import logger
from internal.entities import KittenE
from internal.orm_models import Breed
from internal.orm_models.kitten import Kitten
from internal.repositories import BreedRepo, KittenRepo
from internal.schemas import (
    CreateKittenS,
    KittenID,
    ReturnKittenS,
    UpdateKittenS,
)

KittenId: TypeAlias = int


class KittenService:
    def __init__(
            self,
            kitten_repo: KittenRepo = Depends(),
            breed_repo: BreedRepo = Depends(),
    ):
        self._kitten_repo: KittenRepo = kitten_repo
        self._breed_repo: BreedRepo = breed_repo

    async def get_all_kittens(self, breed: str | None) -> list[ReturnKittenS]:
        if breed:
            return await self.get_kittens_by_breed(breed_name=breed)

        try:
            kittens = await self._kitten_repo.get_all_kittens()
        except DBError as e:
            logger.error(
                msg="failed to get all kittens",
                exc_info=str(e),
            )
            raise e

        res = [
            ReturnKittenS(
                id=kitten.id,
                color=kitten.color,
                age=kitten.age,
                description=kitten.description,
                breed=getattr(kitten.breed, "name", None) or "",
            )
            for kitten in kittens
        ]
        return res

    async def get_kittens_by_breed(
            self, breed_name: str
    ) -> list[ReturnKittenS]:
        try:
            await self._breed_repo.get_breed_by_name(
                name=breed_name
            )
        except NotFoundError as e:
            raise EntityNotFoundError(detail=str(e))
        try:
            kittens = await self._kitten_repo.get_kittens_by_breed(
                breed_name=breed_name
            )
        except DBError as e:
            logger.error(
                msg="failed to get kittens by breed",
                exc_info=str(e),
            )
            raise e
        return [
            ReturnKittenS(
                id=kitten.id,
                color=kitten.color,
                age=kitten.age,
                description=kitten.description,
                breed=getattr(kitten.breed, "name", None) or "",
            )
            for kitten in kittens
        ]

    async def get_kitten(self, id: int) -> ReturnKittenS:
        try:
            kitten: Kitten = await self._kitten_repo.get_kitten_by_id(
            id=id
            )
            return ReturnKittenS(
                id=kitten.id,
                color=kitten.color,
                age=kitten.age,
                description=kitten.description,
                breed=getattr(kitten.breed, "name", None) or ""
            )
        except (NotFoundError, DBError, Exception) as e:
            if type(e) is NotFoundError:
                raise EntityNotFoundError(detail=str(e))
            else:
                logger.error(
                    msg="failed to get kitten",
                    exc_info=str(e),
                )
                raise e

    async def create_kitten(self, create_dto: CreateKittenS) -> KittenID:
        breed_name = create_dto.breed

        create_data: dict = create_dto.model_dump(
            exclude_unset=True, exclude_none=True
        )
        if breed_name:
            # create a kitten, then update its breed (if breed exists)
            try:
                breed: Breed = await self._breed_repo.get_breed_by_name(
                    name=breed_name
                )
            except NotFoundError:
                raise BadRequestError(
                    detail=f"Can't add kitten info: breed {create_dto.breed} wasn't found"  # noqa
                )
            del create_data["breed"]
            try:
                instance_id: int = await self._kitten_repo.create(
                    data=create_data
                )
            except DBError as e:
                    logger.error(
                        msg="failed to create kitten",
                        exc_info=str(e),
                        extra={"create_dto": create_dto},
                    )
                    raise e

            kitten_entity = KittenE(id=instance_id, breed_id=breed.id)
            update_data: dict = kitten_entity.model_dump(
                exclude_none=True, exclude_unset=True
            )
            try:
                await self._kitten_repo.update(
                    data=update_data,
                    instance_id=instance_id
                )  # update breed
            except DBError as e:
                logger.error(msg="failed to update kitten", exc_info=str(e))
                raise e
            return KittenID(
                instance_id=instance_id
            )
        else:
            try:
                instance_id = await self._kitten_repo.create(
                    data=create_data
                )
                return KittenID(
                    instance_id=instance_id
                )
            except DBError as e:
                logger.error(
                    msg="failed to create kitten",
                    exc_info=str(e),
                    extra={"create_dto": create_dto},
                )
                raise e

    async def update_kitten(
            self,
            instance_id: int,
            update_dto: UpdateKittenS
    ) -> ReturnKittenS:
        update_data: dict = update_dto.model_dump(
            exclude_unset=True, exclude_none=True
        )
        if update_dto.breed:
            # if breed doesn't exist, we won't update the kitten
            try:
                breed: Breed = await self._breed_repo.get_breed_by_name(
                    name=update_dto.breed
                )  # if not breed, http_exc will be raised
            except NotFoundError:
                raise BadRequestError(
                    detail=f"Can't perform update: breed '{update_dto.breed}' wasn't found." \
                           " In order to add breed, create it first"  # noqa
                )
            del update_data["breed"]
            update_data["breed_id"] = breed.id  # add id of found breed to \
            # kitten update dict

        try:
            updated_kitten: Kitten = await self._kitten_repo.update(
                data=update_data,
                instance_id=instance_id
            )
            return await self.get_kitten(id=updated_kitten.id)
        except (NotFoundError, DBError, Exception) as e:
            if type(e) is NotFoundError:
                raise EntityNotFoundError(detail=str(e))
            else:
                logger.error(
                    msg="failed to update kitten",
                    exc_info=str(e),
                    extra={"update_dto": update_dto},
                )
                raise e

    async def delete_kitten(self, id: int) -> None:
        try:
            await self._kitten_repo.delete(id=id)
        except (NotFoundError, DBError, Exception) as e:
            if type(e) is NotFoundError:
                raise EntityNotFoundError(detail=str(e))
            else:
                logger.error(
                    msg="failed to delete kitten",
                    exc_info=str(e),
                    extra={"id": id},
                )
                raise e