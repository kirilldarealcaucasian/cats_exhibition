from pydantic import BaseModel, Field


class UpdateBreedS(BaseModel):
    name: str = Field(min_length=1, alias="breed_name")


class CreateBreedS(UpdateBreedS):
    pass


class ReturnBreedS(BaseModel):
    instance_id: int
    name: str


class BreedID(BaseModel):
    instance_id: int

