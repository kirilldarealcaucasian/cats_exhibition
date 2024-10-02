from fastapi import APIRouter, Depends, status

from internal.schemas import BreedID, CreateBreedS, ReturnBreedS
from internal.services import BreedService

router = APIRouter(prefix="/breeds", tags=["Breeds"])


@router.get(
    "",
    response_model=list[ReturnBreedS],
    status_code=status.HTTP_200_OK)
async def get_all_breeds(service: BreedService = Depends()):
    return await service.get_breeds()


@router.post(
    "",
    response_model=BreedID,
    status_code=status.HTTP_201_CREATED
)
async def create_breed(
        create_dto: CreateBreedS,
        service: BreedService = Depends()
):
    return await service.create(create_dto=create_dto)