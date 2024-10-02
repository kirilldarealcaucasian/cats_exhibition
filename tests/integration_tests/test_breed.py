import pytest

from common.exceptions import AlreadyExistsError
from internal.schemas import CreateBreedS, ReturnBreedS
from internal.services import BreedService


@pytest.mark.asyncio(scope="module")
async def test_get_all_breeds(breed_service: BreedService):

    breeds = \
        [CreateBreedS(
            breed_name="сиамская"),
            CreateBreedS(breed_name="бенгальская")
         ]
    for breed in breeds:
        await breed_service.create(
            create_dto=breed
        )

    breeds = await breed_service.get_breeds()

    assert breeds == [
        ReturnBreedS(instance_id=1, name='сиамская'),
        ReturnBreedS(instance_id=2, name='бенгальская')
    ]


@pytest.mark.asyncio(scope="module")
async def test_create_duplicate_breed(breed_service: BreedService):
    with pytest.raises(AlreadyExistsError) as excinfo:
        _ = await breed_service.create(
            create_dto=CreateBreedS(breed_name="бенгальская")
        )
    assert "409: Breed already exists" == str(excinfo.value)




