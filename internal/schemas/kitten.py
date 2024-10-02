from pydantic import BaseModel, ConfigDict, Field


class CreateKittenS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    color: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=0)
    description: str | None = Field(default=None)
    breed: str | None = Field(default=None, min_length=1)


class ReturnKittenS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    color: str | None
    age: int | None
    description: str | None
    breed: str | None


class KittenID(BaseModel):
    instance_id: int


class UpdateKittenS(CreateKittenS):
    pass
