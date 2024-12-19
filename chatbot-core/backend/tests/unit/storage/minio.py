import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest
from minio import Minio
from minio.error import S3Error
from tests.utils import clean_minio_bucket
from tests.utils import validate_config

from app.settings import Constants
from app.settings import Secrets
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


@pytest.fixture
def minio_client() -> Iterator[Minio]:
    """
    Create Minio client
    """
    # Validate the MinIO connection configuration
    validate_config(o=Secrets, required=["MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY"])

    # Create Minio client
    yield Minio(
        endpoint=Secrets.MINIO_ENDPOINT,
        access_key=Secrets.MINIO_ACCESS_KEY,
        secret_key=Secrets.MINIO_SECRET_KEY,
        # TODO: Remove this insecure flag when using a secure connection
        secure=False,
    )


def test_minio_client(minio_client: Minio) -> None:
    """
    Test if the MinIO server is reachable by listing buckets.

    Args:
        minio_client (Minio): Minio client
    """
    try:
        # Check if the server is accessible by listing buckets
        buckets = minio_client.list_buckets()
        assert buckets is not None, "Expected to list buckets, but got None."
    except S3Error as e:
        pytest.fail(f"MinIO error while connecting to Minio: {e}.")
    except Exception as e:
        pytest.fail(f"Unexpected error while connecting to Minio: {e}.")


def test_bucket_exists(minio_client: Minio) -> None:
    """
    Test if a specific bucket exists on the MinIO server.

    Args:
        minio_client (Minio): Minio client
    """
    bucket_name = Constants.MINIO_TEST_BUCKET
    try:
        # Create a new bucket
        minio_client.make_bucket(bucket_name)

        # Verify the bucket was created exists
        buckets = minio_client.list_buckets()
        assert bucket_name in [
            bucket.name for bucket in buckets
        ], f"Expected bucket '{bucket_name}' to be exist, but it was not."
    except S3Error as e:
        pytest.fail(
            f"MinIO error while uploading file: {e}. Bucket '{bucket_name}' does not exist."
        )
    except Exception as e:
        pytest.fail(
            f"Unexpected error while checking if bucket exists: {e}. Bucket '{bucket_name}' does not exist."
        )
    finally:
        # Clean up the bucket
        clean_minio_bucket(minio_client=minio_client, bucket_name=bucket_name)


def test_upload_file(minio_client: Minio) -> None:
    """
    Test uploading a file to the MinIO server.

    Args:
        minio_client (Minio): Minio client
    """
    bucket_name = Constants.MINIO_TEST_BUCKET
    object_name = Constants.MINIO_TEST_UPLOADED_OBJECT_NAME
    file_content = Constants.MINIO_TEST_FILE_CONTENT

    # Create a temporary file with the file content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        file_path = temp_file.name

    try:
        # Create a new bucket
        minio_client.make_bucket(bucket_name)

        # Upload file to the bucket
        minio_client.fput_object(
            bucket_name=bucket_name, object_name=object_name, file_path=file_path
        )

        # Verify the file exists in the bucket
        uploaded_objects = minio_client.list_objects(bucket_name=bucket_name)
        uploaded_object = next(
            (
                uploaded_object
                for uploaded_object in uploaded_objects
                if uploaded_object.object_name == object_name
            ),
            None,
        )
        assert (
            uploaded_object is not None
        ), f"Expected file '{object_name}' to be uploaded to bucket '{bucket_name}', but it was not."
    except S3Error as e:
        pytest.fail(
            f"MinIO error while uploading file: {e}. File '{object_name}' could not be uploaded to bucket '{bucket_name}'."
        )
    except Exception as e:
        pytest.fail(
            f"Unexpected error while uploading file: {e}. File '{file_path}' could not be uploaded to bucket '{bucket_name}'."
        )
    finally:
        # Clean up the bucket and temporary file
        clean_minio_bucket(minio_client=minio_client, bucket_name=bucket_name)
        Path(file_path).unlink()


def test_download_file(minio_client: Minio) -> None:
    """
    Test downloading a file from the MinIO server.

    Args:
        minio_client (Minio): Minio client
    """
    bucket_name = Constants.MINIO_TEST_BUCKET
    object_name = Constants.MINIO_TEST_UPLOADED_OBJECT_NAME
    file_content = Constants.MINIO_TEST_FILE_CONTENT

    # Create a temporary original file with the file content
    with tempfile.NamedTemporaryFile(delete=False) as temp_original_file:
        temp_original_file.write(file_content)
        original_file_path = Path(temp_original_file.name)

    try:
        # Create a new bucket
        minio_client.make_bucket(bucket_name)

        # Upload file to the bucket
        minio_client.fput_object(
            bucket_name=bucket_name, object_name=object_name, file_path=original_file_path
        )

        # Download file from the bucket
        response = minio_client.get_object(
            bucket_name=Constants.MINIO_TEST_BUCKET,
            object_name=object_name,
        )

        # Create a temporary file which will be downloaded
        with tempfile.NamedTemporaryFile(delete=False) as temp_downloaded_file:
            temp_downloaded_file.write(response.read())
            downloaded_file_path = Path(temp_downloaded_file.name)

        # Verify the file was downloaded
        assert (
            downloaded_file_path.exists()
        ), f"Expected file '{object_name}' to be downloaded, but it was not."

        # Verify the contents of the downloaded file is the same as the original file
        with (
            original_file_path.open("rb") as original_file,
            downloaded_file_path.open("rb") as downloaded_file,
        ):
            original_content = original_file.read()
            downloaded_content = downloaded_file.read()
            assert (
                original_content == downloaded_content
            ), f"Expected downloaded file content to match the original file, got {downloaded_content} instead of {original_content}."
    except S3Error as e:
        pytest.fail(
            f"MinIO error while downloading file: {e}. File '{object_name}' could not be downloaded from bucket '{Constants.MINIO_TEST_BUCKET}'."
        )
    except Exception as e:  # Catch unexpected exceptions
        pytest.fail(
            f"Unexpected error while downloading file: {e}. File '{object_name}' could not be downloaded from bucket '{Constants.MINIO_TEST_BUCKET}'."
        )
    finally:
        # Clean up the bucket, temporary files, and downloaded file
        clean_minio_bucket(minio_client=minio_client, bucket_name=bucket_name)
        original_file_path.unlink()
        downloaded_file_path.unlink()


def test_delete_file(minio_client: Minio) -> None:
    """
    Test deleting a file from the MinIO server.

    Args:
        minio_client (Minio): Minio client
    """
    bucket_name = Constants.MINIO_TEST_BUCKET
    object_name = Constants.MINIO_TEST_UPLOADED_OBJECT_NAME
    file_content = Constants.MINIO_TEST_FILE_CONTENT

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        file_path = temp_file.name

    try:
        # Create a new bucket
        minio_client.make_bucket(bucket_name)

        # Upload file to the bucket
        minio_client.fput_object(
            bucket_name=bucket_name, object_name=object_name, file_path=file_path
        )

        # Delete the file from the bucket
        minio_client.remove_object(bucket_name=bucket_name, object_name=object_name)

        # Verify the file was deleted
        uploaded_objects = minio_client.list_objects(bucket_name=bucket_name)
        uploaded_object = next(
            (
                uploaded_object
                for uploaded_object in uploaded_objects
                if uploaded_object.object_name == object_name
            ),
            None,
        )
        assert (
            uploaded_object is None
        ), f"Expected file '{object_name}' to be deleted from bucket '{bucket_name}', but it was not."
    except S3Error as e:
        pytest.fail(
            f"MinIO error while deleting file: {e}. File '{object_name}' could not be deleted from bucket '{bucket_name}'."
        )
    except Exception as e:
        pytest.fail(
            f"Unexpected error while deleting file: {e}. File '{object_name}' could not be deleted from bucket '{bucket_name}'."
        )
    finally:
        # Clean up the bucket and temporary file
        clean_minio_bucket(minio_client=minio_client, bucket_name=bucket_name)
        Path(file_path).unlink()
