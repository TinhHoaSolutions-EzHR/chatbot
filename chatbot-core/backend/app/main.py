from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.databases.minio import MinioConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.routers import base
from app.routers.v1 import connector
from app.settings import Constants
from app.utils.llama_index_configuration import init_llamaindex_configurations
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifespan event handler

    Args:
        app (FastAPI): FastAPI application instance
    """
    # Initialize the Minio, Qdrant, and Redis connectors
    app.state.minio_conn = MinioConnector()
    app.state.qdrant_conn = QdrantConnector()
    app.state.redis_conn = RedisConnector()

    # Initialize the LlamaIndex configuration (LLM and Embedding models)
    init_llamaindex_configurations(
        llm_model=Constants.LLM_MODEL,
        embedding_model=Constants.EMBEDDING_MODEL,
    )

    try:
        yield
    finally:
        # Close the Qdrant, and Redis connectors (Minio is closed automatically)
        app.state.qdrant_conn.client.close()
        app.state.redis_conn.client.close()


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
