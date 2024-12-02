from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import base
from app.routers.v1 import connector
from app.settings.constants import Constants
from app.utils.llama_index_configuation import init_llamaindex_config
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifespan event handler

    Args:
        app (FastAPI): FastAPI application instance
    """
    # Initialize the LlamaIndex configuration (LLM and Embedding models)
    init_llamaindex_config()
    yield


def create_app() -> FastAPI:
    """
    Construct and configure the FastAPI application
    """

    # Initialize FastAPI application
    app = FastAPI(
        title=Constants.FASTAPI_NAME,
        version=Constants.FASTAPI_VERSION,
        description=Constants.FASTAPI_DESCRIPTION,
        lifespan=lifespan,
    )

    logger.info(f"API {Constants.FASTAPI_NAME} {Constants.FASTAPI_VERSION} started successfully")

    # Include application routers
    app.include_router(router=base.router)
    app.include_router(router=connector.router, prefix=Constants.FASTAPI_PREFIX)

    return app


app = create_app()
