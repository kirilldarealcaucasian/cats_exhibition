from typing import TypeAlias

from fastapi import APIRouter, Depends, Query, status

from internal.schemas import (
    CreateKittenS,
    KittenID,
    ReturnKittenS,
    UpdateKittenS,
)
from internal.services import KittenService

router = APIRouter(prefix="/kittens", tags=["Kittens"])

KittenId: TypeAlias = int


@router.get("",
            response_model=list[ReturnKittenS],
            status_code=status.HTTP_200_OK,
            description="Get all kittens")
async def get_all_kittens(
    breed: str = Query(None),
    service: KittenService = Depends()
):
    return await service.get_all_kittens(breed=breed)


@router.get(
    "/{id}",
    response_model=ReturnKittenS,
    status_code=status.HTTP_200_OK,
    description="Get kitten info"
)
async def get_kitten_info(id: int, service: KittenService = Depends()):
    return await service.get_kitten(id=id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=KittenID,
    description="Add information about kitten"
)
async def create_kitten(
    create_dto: CreateKittenS, service: KittenService = Depends()
):
    return await service.create_kitten(create_dto=create_dto)


@router.patch(
    "/{id}",
    response_model=ReturnKittenS,
    status_code=status.HTTP_200_OK,
    description="Update information about kitten"
)
async def update_kitten(
    id: int,
    update_dto: UpdateKittenS, service: KittenService = Depends()
):
    return await service.update_kitten(
        instance_id=id, update_dto=update_dto
    )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete information about kitten"
)
async def delete_kitten(
        id: int,
        service: KittenService = Depends()
) -> None:
    return await service.delete_kitten(id=id)
