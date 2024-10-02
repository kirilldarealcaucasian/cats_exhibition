import asyncio

import pytest
import pytest_asyncio

from internal.orm_models import Base
from internal.repositories import BreedRepo, KittenRepo
from internal.services import BreedService, KittenService
from internal.storage import db_client


@pytest.fixture(scope="session")
def kitten_service() -> KittenService:
    kitten_repo = KittenRepo()
    breed_repo = BreedRepo()
    return KittenService(
        kitten_repo=kitten_repo,
        breed_repo=breed_repo
    )


@pytest.fixture(scope="session")
def breed_service() -> BreedService:
    breed_repo = BreedRepo()
    return BreedService(
        breed_repo=breed_repo
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with db_client.engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()