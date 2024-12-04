from typing import List

from minio import Minio


def validate_config(o: object, required: List[str]) -> None:
    """
    Validate connection configuration

    Args:
        o (object): The object to validate
        required (List[str]): The list of required attributes

    Raises:
        ValueError: If any of the required attributes are missing
    """
    missing = [k for k in required if not getattr(o, k, None)]
    if missing:
        raise ValueError(f"Missing required connection configuration: {', '.join(missing)}")


def clean_minio_bucket(minio_client: Minio, bucket_name: str) -> None:
    """
    Clean the bucket by removing all objects and then deleting the bucket.

    Args:
        minio_client (Minio): Minio client
        bucket_name (str): The name of the bucket to clean
    """
    # List all objects in the bucket and remove them
    objects = minio_client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        minio_client.remove_object(bucket_name, obj.object_name)

    # Remove the bucket
    minio_client.remove_bucket(bucket_name)
