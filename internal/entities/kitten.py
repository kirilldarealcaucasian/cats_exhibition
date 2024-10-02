from pydantic import BaseModel, Field


class KittenE(BaseModel):
    id: int | None = Field(default=None, ge=0)
    color: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, ge=0)
    breed_id: int | None = Field(default=None, ge=0)
