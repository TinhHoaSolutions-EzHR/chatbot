import os
from datetime import datetime
from typing import Literal

from app.utils.string import remove_vietnamese_accents


def construct_file_path(
    object_name: str,
    bucket_name: str,
    user_id: str = None,
    file_extension: Literal["pdf", "png", "jpg", "jpeg"] = "png",
) -> str:
    """
    Construct file path in Minio.

    Args:
        object_name (str): Name of the object.
        bucket_name (str): Name of the bucket.
        user_id (str): User id. Defaults to None.
        file_extension (str): File extension. Defaults to "png".

    Returns:
        str: File path in Minio.

    Example:
        >>> construct_file_path(
        ...     object_name="document", bucket_name="documents", user_id="1", file_extension="pdf"
        ... )
        >>> # "documents/document_1_20211001120000.pdf"
    """
    file_name = remove_vietnamese_accents(input_str=object_name).replace(" ", "_").lower()
    if user_id:
        file_name += f"_{user_id}"

    file_name += f"_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
    file_path = os.path.join(bucket_name, file_name)

    return file_path
