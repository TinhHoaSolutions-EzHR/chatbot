from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.settings import Constants
from app.settings import Secrets
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class PostgresConnector:
    """
    Pattern: Singleton
    Purpose: Create a single instance of the database connection
    """

    _instance = None

    def __init__(self):
        if PostgresConnector._instance is None:
            PostgresConnector._instance = self.__create_engine()

    @classmethod
    def get_instance(cls):
        """
        Get the instance of the database connection
        """
        if cls._instance is None:
            cls._instance = cls().__create_engine()
        return cls._instance

    @classmethod
    def __create_engine(cls):
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


def get_session() -> Session:
    """
    Generate a database session for the applications
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
