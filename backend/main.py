from fastapi import FastAPI

from databases.postgres import PostgresConnector
from utils import logger
from routers import base
from routers.v1 import chat, embedding_model
from settings import Constants

logger = logger.LoggerFactory(__name__).get_logger()

app = FastAPI(
    title=Constants.API_NAME,
    version=Constants.API_VERSION,
    description=Constants.API_DESCRIPTION,
)

postgres_instance = PostgresConnector.get_instance()

logger.info(f"API {Constants.API_NAME} {Constants.API_VERSION} started successfully")

app.include_router(base.router)
app.include_router(chat.router, prefix=Constants.API_PREFIX)
app.include_router(embedding_model.router, prefix=Constants.API_PREFIX)