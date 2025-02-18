from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex

from app.databases.minio import MinioConnector
from app.databases.qdrant import QdrantConnector
from app.databases.redis import RedisConnector
from app.routers import auth
from app.routers import base
from app.routers.v1 import agent
from app.routers.v1 import background
from app.routers.v1 import chat
from app.routers.v1 import connector
from app.routers.v1 import folder
from app.routers.v1 import provider
from app.routers.v1 import user
from app.seeds import get_seeder_config
from app.seeds import seed_db
from app.settings import Constants
from app.utils.api.helpers import get_logger
from app.utils.llm.helpers import init_llm_configurations

logger = get_logger(__name__)

index = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI application lifespan event handler

    Args:
        app (FastAPI): FastAPI application instance
    """
    # Seed the database on startup if the configuration is set
    config = get_seeder_config()
    if config.SEED_ON_STARTUP:
        seed_db()

    # Initialize the Minio, Qdrant, and Redis connectors
    app.state.minio_conn = MinioConnector()
    app.state.qdrant_conn = QdrantConnector()
    app.state.redis_conn = RedisConnector()

    # Initialize the LlamaIndex configuration (LLM and Embedding models)
    init_llm_configurations(
        llm_model=Constants.LLM_MODEL,
        embedding_model=Constants.EMBEDDING_MODEL,
    )

    # TODO: Remove it as this is just a work around
    global index

    documents = SimpleDirectoryReader("examples/").load_data()
    index = VectorStoreIndex.from_documents(documents=documents)

    try:
        yield
    finally:
        # Close the Qdrant, and Redis connectors (Minio is closed automatically)
        app.state.qdrant_conn.client.close()
        app.state.redis_conn.client.close()


def create_app() -> FastAPI:
    """
    Construct and configure the FastAPI application

    Returns:
        FastAPI: FastAPI application instance
    """

    # Initialize FastAPI application
    app = FastAPI(
        title=Constants.FASTAPI_NAME,
        version=Constants.FASTAPI_VERSION,
        description=Constants.FASTAPI_DESCRIPTION,
        lifespan=lifespan,
    )
    origins = [
        "http://127.0.0.1:3000",
    ]  # WARN: Update this to the actual frontend URL

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include application routers
    logger.info("Including routers")
    app.include_router(router=base.router)
    app.include_router(router=auth.router)
    app.include_router(router=connector.router, prefix=Constants.FASTAPI_PREFIX)
    app.include_router(router=chat.router, prefix=Constants.FASTAPI_PREFIX)
    app.include_router(router=folder.router, prefix=Constants.FASTAPI_PREFIX)
    app.include_router(router=agent.router, prefix=Constants.FASTAPI_PREFIX)
    app.include_router(router=user.router, prefix=Constants.FASTAPI_PREFIX)
    app.include_router(router=provider.router, prefix=Constants.FASTAPI_PREFIX)
    app.include_router(router=background.router, prefix=Constants.FASTAPI_PREFIX)

    logger.info(
        f"API {Constants.FASTAPI_NAME} version {Constants.FASTAPI_VERSION} started successfully"
    )

    return app


app = create_app()
