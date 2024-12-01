import contextlib
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import AsyncGenerator, Iterator

from app.databases.base import BaseConnector
from app.utils.logger import LoggerFactory
from app.settings import Constants, Secrets

logger = LoggerFactory().get_logger(__name__)


class MSSQLConnector(BaseConnector[Engine]):
    """
    MSSQL connector class

    Pattern: Singleton
    Purpose: Create a single instance of the database connection
    """

    _o = Secrets
    _required_keys = ["MSSQL_USER", "MSSQL_SA_PASSWORD", "MSSQL_HOST", "MSSQL_DB"]

    @classmethod
    def _create_client(cls) -> Engine:
        """
        Create the database connection if there is no any existing connection

        Returns:
            Engine: Database connection instance
        """
        try:
            uri = Constants.MSSQL_CONNECTOR_URI.format(
                user=Secrets.MSSQL_USER,
                password=Secrets.MSSQL_SA_PASSWORD,
                host=Secrets.MSSQL_HOST,
                db_name=Secrets.MSSQL_DB,
                driver=Constants.MSSQL_DRIVER,
            )
            return create_engine(
                uri,
                pool_size=Constants.MSSQL_POOL_SIZE,
                max_overflow=Constants.MSSQL_MAX_OVERFLOW,
                pool_timeout=Constants.MSSQL_POOL_TIMEOUT,
                pool_recycle=Constants.MSSQL_POOL_RECYCLE,
            )
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise


@contextlib.contextmanager
def get_db_connector() -> Iterator[MSSQLConnector]:
    """
    Get the database connection

    Yields:
        Engine: Database connection instance
    """
    connector = MSSQLConnector()
    yield connector


# Get the engine from the MSSQLConnector singleton
with get_db_connector() as connector:
    engine = connector.client

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db_session() -> AsyncGenerator[Session, None]:
    """
    Provides a transactional scope around a series of operations.

    Yields:
        Session: Database session

    Raises:
        Exception: Any exception that occurs during the database session
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
