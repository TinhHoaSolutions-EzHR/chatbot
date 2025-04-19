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


class PostgresConnector(BaseConnector[Engine]):
    """
    PostgreSQL connector class

    Pattern: Singleton
    Purpose: Create a single instance of the database connection
    """

    _o = Secrets
    _required_keys = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_DB"]

    @classmethod
    def _create_client(cls) -> Engine:
        """
        Create the database connection if there is no any existing connection

        Returns:
            Engine: Database connection instance
        """
        try:
            url = Constants.POSTGRES_CONNECTOR_URI.format(
                user=Secrets.POSTGRES_USER,
                password=Secrets.POSTGRES_PASSWORD,
                host=Secrets.POSTGRES_HOST,
                port=Secrets.POSTGRES_PORT,
                db_name=Secrets.POSTGRES_DB,
            )

            return create_engine(
                url=url,
                pool_size=Constants.DATABASE_POOL_SIZE,
                max_overflow=Constants.DATABASE_MAX_OVERFLOW,
                pool_timeout=Constants.DATABASE_POOL_TIMEOUT,
                pool_recycle=Constants.DATABASE_POOL_RECYCLE,
            )
        except Exception as e:
            logger.error(f"Error initializing database: {e}", exc_info=True)

    @classmethod
    def get_engine(cls) -> Engine:
        """
        Get the database connection instance

        Returns:
            Engine: Database connection instance
        """
        if not cls._client:
            with cls._lock:
                cls._client = cls._create_client()

        return cls._client


# Create a session maker
SessionLocal = sessionmaker(
    bind=PostgresConnector.get_engine(),
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
        try:
            yield session
        except Exception as e:
            logger.error(f"An unexpected error during database session: {str(e)}")
            raise e
        finally:
            session.close()
