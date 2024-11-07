from fastapi import FastAPI

from utils import logger
from routers import base
from routers.v1 import embedding_model
from settings import Constants

logger = logger.LoggerFactory().get_logger(__name__)


def create_app() -> FastAPI:
    """
    Construct and configure the FastAPI application
    """
    # Initialize FastAPI application
    app = FastAPI(
        title=Constants.API_NAME,
        version=Constants.API_VERSION,
        description=Constants.API_DESCRIPTION,
    )

    logger.info(
        f"API {Constants.API_NAME} {Constants.API_VERSION} started successfully"
    )

    # Include application routers
    app.include_router(router=base.router)
    app.include_router(router=embedding_model.router, prefix=Constants.API_PREFIX)

    return app


app = create_app()
