from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from utils.logger import LoggerFactory
from settings import Constants, Secrets

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

    @staticmethod
    def __create_engine():
        """
        Create the database connection if there is no any existing connection
        """
        try:
            return create_engine(
                Secrets.POSTGRES_URI,
                pool_size=Constants.POOL_SIZE,
                max_overflow=Constants.MAX_OVERFLOW,
                pool_timeout=Constants.POOL_TIMEOUT,
                pool_recycle=Constants.POOL_RECYCLE,
            )
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise


# Get the engine from the PostgresConnector singleton
engine = PostgresConnector.get_instance()

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """
    Generate a database session for the applications
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
