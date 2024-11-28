import os
from minio import Minio
from minio.error import S3Error
from typing import BinaryIO

from app.settings import Secrets
from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


class MinioConnector:
    """
    Minio connector class

    Pattern: Singleton
    Purpose: Create a single instance of the object storage connection
    """

    _instance = None
    _minio_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MinioConnector, cls).__new__(cls)
            cls._minio_client = cls._create_minio_client()
        return cls._instance

    @property
    def client(self) -> Minio:
        """
        Get the Minio client instance
        """
        return self._minio_client

    @classmethod
    def get_instance(cls) -> "MinioConnector":
        """
        Get the instance of the MinioConnector
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def _create_minio_client() -> Minio:
        """
        Create the object storage connection if there is no any existing connection
        """
        try:
            return Minio(
                endpoint=Secrets.MINIO_ENDPOINT,
                access_key=Secrets.MINIO_ACCESS_KEY,
                secret_key=Secrets.MINIO_SECRET_KEY,
                secure=False,
            )
        except S3Error as e:
            logger.error(f"Error initializing object storage: {e}")
            raise

    def create_bucket(self, bucket_name: str) -> None:
        """
        Create a bucket in object storage
        """
        found = self.client.bucket_exists(bucket_name=bucket_name)
        if not found:
            logger.info(f"Bucket {bucket_name} not found. Creating...")
            self.client.make_bucket(bucket_name)
        else:
            logger.info(f"Bucket {bucket_name} already exists")

    def upload_files(self, object_name: str, data: BinaryIO, bucket_name: str, length: int = None) -> None:
        """
        Upload files to object storage
        """
        try:
            # Create the bucket if it does not exist
            self.create_bucket(bucket_name=bucket_name)

            # Get the current position of the file pointer
            current_pos = data.tell()

            # If length is not provided, try to calculate it
            if length is None:
                # Seek to the end to get the file size
                data.seek(0, os.SEEK_END)
                length = data.tell() - current_pos
                # Reset the file pointer to its original position
                data.seek(current_pos)

            # Upload the file to the bucket
            self.client.put_object(bucket_name=bucket_name, object_name=object_name, data=data, length=length)
        except Exception as e:
            logger.error(f"Error uploading file {object_name}: {e}")
            raise


def get_object_storage_client() -> MinioConnector:
    """
    Get the instance of MinioConnector
    """
    return MinioConnector.get_instance()
