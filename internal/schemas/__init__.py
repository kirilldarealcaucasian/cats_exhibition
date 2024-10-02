__all__ = (
    "CreateKittenS", "ReturnKittenS",
    "UpdateKittenS", "UpdateBreedS",
    "CreateBreedS", "ReturnBreedS",
    "KittenID", "BreedID",
)

from .breed import BreedID, CreateBreedS, ReturnBreedS, UpdateBreedS
from .kitten import CreateKittenS, KittenID, ReturnKittenS, UpdateKittenS
