from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .breed import Breed


class Kitten(Base):
    __tablename__ = "kittens"

    color: Mapped[str]
    age: Mapped[int]
    description: Mapped[str | None]
    breed_id: Mapped[int | None] = mapped_column(
        ForeignKey("breeds.id", ondelete="RESTRICT"), index=True
    )

    # relationships
    breed: Mapped["Breed"] = relationship(back_populates="kittens")

    def __repr__(self):
        return f"Kitten(\
        id={self.id}, color={self.color}, age={self.age},\
         description={self.description}, breed_id={self.breed_id})"
