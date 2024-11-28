from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.utils.logger import LoggerFactory
from app.settings import Constants, Secrets

logger = LoggerFactory().get_logger(__name__)


class MSSQLConnector:
    """
    MSSQL connector class

    Pattern: Singleton
    Purpose: Create a single instance of the database connection
    """

    _instance: Engine = None

    @classmethod
    def get_instance(cls) -> Engine:
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
            uri = Constants.MSSQL_CONNECTOR_URI.format(
                user=Secrets.MSSQL_USER,
                password=Secrets.MSSQL_SA_PASSWORD,
                host=Secrets.MSSQL_HOST,
                port=Secrets.MSSQL_PORT,
                db_name=Secrets.MSSQL_DB_NAME,
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


# Get the engine from the MSSQLConnector singleton
engine = MSSQLConnector.get_instance()

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
