from collections.abc import Generator

from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.databases.base import BaseConnector
from app.settings import Constants
from app.settings import Secrets
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


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
            url = Constants.MSSQL_CONNECTOR_URI.format(
                user=Secrets.MSSQL_USER,
                password=Secrets.MSSQL_SA_PASSWORD,
                host=Secrets.MSSQL_HOST,
                db_name=Secrets.MSSQL_DB,
                driver=Constants.MSSQL_DRIVER,
            )
            return create_engine(
                url=url,
                pool_size=Constants.MSSQL_POOL_SIZE,
                max_overflow=Constants.MSSQL_MAX_OVERFLOW,
                pool_timeout=Constants.MSSQL_POOL_TIMEOUT,
                pool_recycle=Constants.MSSQL_POOL_RECYCLE,
            )
        except Exception as e:
            logger.error(f"Error initializing database: {e}", exc_info=True)


# Create a session maker
SessionLocal = sessionmaker(
    bind=MSSQLConnector().client,
    expire_on_commit=False,
    class_=Session,
    autoflush=False,
    autocommit=False,
)


def get_db_session() -> Generator[Session]:
    """
    Provides a transactional scope around a series of operations.

    Yields:
        Session: Database session

    Raises:
        Exception: Any exception that occurs during the database session
    """
    with SessionLocal() as session:
        yield session
