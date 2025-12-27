from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, FastAPI, Response

from src.api.zk import zk
from src.services import telegram


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any, Any]:
    """Startup and shutdown code to run around the lifespan of the FastAPI app. These calls will execute per app, per worker. Anything called here will not be indempotent between workers"""
    await telegram.start_application()
    yield
    await telegram.stop_application()


app = FastAPI(lifespan=lifespan)

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(zk)


@v1_router.get("/status/checkhealth")
async def checkhealth() -> Response:
    """Returns a simple 200 health response."""
    return Response()


app.include_router(v1_router)
