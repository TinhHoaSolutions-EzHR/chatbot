from fastapi import FastAPI

from utils.logger import LoggerFactory
from routers import base
from routers.v1 import embedding_model
from settings import Constants

logger = LoggerFactory().get_logger(__name__)


def create_app() -> FastAPI:
    """
    Construct and configure the FastAPI application
    """
    # Initialize FastAPI application
    app = FastAPI(
        title=Constants.FASTAPI_NAME,
        version=Constants.FASTAPI_VERSION,
        description=Constants.FASTAPI_DESCRIPTION,
    )

    logger.info(
        f"API {Constants.FASTAPI_NAME} {Constants.FASTAPI_VERSION} started successfully"
    )

    # Include application routers
    app.include_router(router=base.router)
    app.include_router(router=embedding_model.router, prefix=Constants.FASTAPI_PREFIX)

    return app


app = create_app()
