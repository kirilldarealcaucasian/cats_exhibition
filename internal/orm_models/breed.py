from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .kitten import Kitten


class Breed(Base):
    __tablename__ = "breeds"

    name: Mapped[str] = mapped_column(unique=True)

    # relationships
    kittens: Mapped[list["Kitten"]] = relationship(back_populates="breed")

    def __repr__(self):
        return f"Breed(id={self.id}, name={self.name})"
