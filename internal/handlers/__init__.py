__all__ = (
    "kittens_router",
    "breeds_router",
)
from .breed_handlers import router as breeds_router
from .kitten_handlers import router as kittens_router
