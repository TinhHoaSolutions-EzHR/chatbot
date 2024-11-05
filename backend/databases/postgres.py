import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.logger import LoggerFactory
from settings import Secrets

logger = LoggerFactory.get_logger(__name__)

class PostgresConnector:
    _instance = None

    def __init__(self):
        if PostgresConnector._instance is None:
            PostgresConnector._instance = self.__create_engine()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls().__create_engine()
        return cls._instance

    @staticmethod
    def __create_engine():
        try:
            return create_engine(
                Secrets.POSTGRES_DB_URI,
                pool_size=100,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600
            )
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
