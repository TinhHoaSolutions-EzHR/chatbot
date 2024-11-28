from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.utils.logger import LoggerFactory
from app.settings import Constants, Secrets

logger = LoggerFactory().get_logger(__name__)


class PostgresConnector:
    """
    Postgres connector class

    Pattern: Singleton
    Purpose: Create a single instance of the database connection
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the instance of the database connection
        """
        if cls._instance is None:
            cls._instance = cls()._create_engine()

        return cls._instance

    @classmethod
    def _create_engine(cls) -> Engine | None:
        """
        Create the database connection if there is no any existing connection
        """
        try:
            uri = Constants.POSTGRES_CONNECTOR_URI.format(
                user=Secrets.POSTGRES_USER,
                password=Secrets.POSTGRES_PASSWORD,
                host=Secrets.POSTGRES_HOST,
                port=Secrets.POSTGRES_PORT,
                name=Secrets.POSTGRES_NAME,
            )
            return create_engine(
                uri,
                pool_size=Constants.POSTGRES_POOL_SIZE,
                max_overflow=Constants.POSTGRES_MAX_OVERFLOW,
                pool_timeout=Constants.POSTGRES_POOL_TIMEOUT,
                pool_recycle=Constants.POSTGRES_POOL_RECYCLE,
            )
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise


# Get the engine from the PostgresConnector singleton
engine = PostgresConnector.get_instance()

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    """
    Generate a database session for the applications
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
