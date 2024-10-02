from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from common.logger import logger
from internal.handlers import breeds_router, kittens_router
from internal.orm_models import Base
from internal.storage import db_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_client._engine.begin() as con:  # create tables
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
        logger.info(msg="tables have been created")
    yield


app = FastAPI(lifespan=lifespan)

for router in (kittens_router, breeds_router):
    app.include_router(router)


@app.get("/")
def home() -> dict:
    return {"message": "hello"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_errors(request: Request, call_next):
    """multiplexes unprocessed errors into error with status code 500"""
    try:
        response = await call_next(request)
    except Exception as e:
        if not isinstance(e, HTTPException):
            logger.error(
                msg="something went wrong",
                exc_info=str(e),
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "something went wrong"},
            )
        raise e
    return response


if __name__ == "__main__":
    uvicorn.run("internal.run:app", reload=True)
