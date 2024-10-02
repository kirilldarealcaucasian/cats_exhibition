import pytest

from common.exceptions import BadRequestError, EntityNotFoundError
from internal.schemas import (
    CreateBreedS,
    CreateKittenS,
    KittenID,
    ReturnKittenS,
    UpdateKittenS,
)
from internal.services import BreedService, KittenService


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize(
    "data,res",
    [
        ({"color": "серый", "age": 2, "description": ""},
         ReturnKittenS(
             id=1,
             color="серый",
             age=2,
             description="",
             breed=""
         )),
        ({"color": "белый", "age": 0, "description": "description"},
         ReturnKittenS(
             id=2,
             color="белый",
             age=0,
             description="description",
             breed=""
         ))
    ]
)
async def test_create_kitten_without_breed(
        data: dict,
        res: ReturnKittenS,
        kitten_service: KittenService,
):
    example_kitten = CreateKittenS(
        **data
    )
    kitten_id: KittenID = await kitten_service.create_kitten(
        create_dto=example_kitten
    )

    assert kitten_id.instance_id == res.id

    kittens: list[ReturnKittenS] = await kitten_service.get_all_kittens(
        breed=None
    )

    if res not in kittens:
        pytest.fail(msg="No kitten in the result list")


@pytest.mark.asyncio(scope="session")
async def test_create_kitten_with_breed_error(kitten_service: KittenService):
    kitten_dto = CreateKittenS(
        color="серый",
        age=2,
        description="",
        breed="британский"
    )

    with pytest.raises(BadRequestError) as excinfo:
        await kitten_service.create_kitten(
            create_dto=kitten_dto
        )

    assert "Can't add kitten info: breed британский wasn't found" \
           == str(excinfo.value)


@pytest.mark.asyncio(scope="session")
async def test_create_kitten_with_breed_success(
        kitten_service: KittenService,
        breed_service: BreedService
):
    breed_dto = CreateBreedS(
        breed_name="британский"
    )
    await breed_service.create(
        create_dto=breed_dto
    )

    kitten_dto = CreateKittenS(
        color="серый",
        age=2,
        description="",
        breed="британский"
    )

    await kitten_service.create_kitten(
        create_dto=kitten_dto
    )

    kittens: list[ReturnKittenS] = await kitten_service.get_all_kittens(
        breed=None
    )

    if ReturnKittenS(
            id=3,
            color="серый",
            age=2,
            description="",
            breed="британский"
    ) not in kittens:
        pytest.fail(msg="No kitten in the result list")


@pytest.mark.asyncio(scope="session")
@pytest.mark.parametrize(
    "instance_id,update_data,res",
    [(1, {"breed": "британский"}, ReturnKittenS(
        id=1,
        color="серый",
        age=2,
        description="",
        breed="британский"
    )),
     (2, {"age": 5, "description": "любит играть"}, ReturnKittenS(
         id=2,
         color="белый",
         age=5,
         description="любит играть",
         breed=""
     ))
     ]
)
async def test_update_kitten(
        kitten_service: KittenService,
        update_data: dict,
        res: ReturnKittenS,
        instance_id: int
):
    update_dto = UpdateKittenS(**update_data)
    updated_kitten: ReturnKittenS = await kitten_service.update_kitten(
        instance_id=instance_id,
        update_dto=update_dto,
    )
    assert updated_kitten == res


@pytest.mark.asyncio(scope="session")
async def test_get_all_kittens(kitten_service: KittenService):
    kittens = await kitten_service.get_all_kittens(breed=None)

    assert kittens == [
        ReturnKittenS(
            id=3, color='серый', age=2,
            description='', breed='британский'
        ),
        ReturnKittenS(
            id=1, color='серый', age=2,
            description='', breed='британский'
        ),
        ReturnKittenS(
            id=2, color='белый', age=5,
            description='любит играть', breed=''
        )
    ]

    kittens_by_breed = await kitten_service.get_all_kittens(breed="британский")
    assert kittens_by_breed == [
        ReturnKittenS(
            id=3, color='серый', age=2,
            description='', breed='британский'
        ),
        ReturnKittenS(
            id=1, color='серый', age=2, description='',
            breed='британский'
        )
    ]


async def test_get_kitten_by_breed_error(kitten_service: KittenService):
    with pytest.raises(EntityNotFoundError) as excinfo:
        _ = await kitten_service \
            .get_all_kittens(
            breed="ssss"
        )

    assert "404: Breed wasn't found" == str(excinfo.value)


async def test_get_kitten_info(kitten_service: KittenService):
    kitten = await kitten_service.get_kitten(id=1)

    assert kitten == ReturnKittenS(
        id=1,
        color='серый',
        age=2,
        description='',
        breed='британский',

    )

    with pytest.raises(EntityNotFoundError) as excinfo:
        not_existent_kitten = await kitten_service.get_kitten(id=100)  # noqa
    assert "404: Kitten wasn't found" == str(excinfo.value)


@pytest.mark.asyncio(scope="session")
async def test_delete_kitten(kitten_service: KittenService):
    _ = await kitten_service.delete_kitten(id=1)

    with pytest.raises(EntityNotFoundError) as excinfo:
        _ = await kitten_service.get_kitten(id=1)

    assert "404: Kitten wasn't found" == str(excinfo.value)

    with pytest.raises(EntityNotFoundError) as excinfo2:
        _ = await kitten_service.delete_kitten(id=100)
    assert "404: Kitten wasn't found" == str(excinfo2.value)
