import os
from datetime import datetime
from enum import Enum


class FileExtension(Enum):
    """
    Enumeration of file extensions.
    """

    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"


S1 = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ"
S0 = "AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy"


def remove_vietnamese_accents(input_str: str) -> str:
    """
    Remove Vietnamese accents from a string.

    Args:
        input_str (str): Input string with accents.

    Returns:
        str: Output string without accents.
    """

    return "".join([S0[S1.index(c)] if c in S1 else c for c in input_str])


def construct_file_path(
    object_name: str, bucket_name: str, user_id: str = None, file_extension: str = FileExtension.PNG
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
        >>> construct_file_path("
        # my_avatar_f6f7b43c-c0ca-4003-8143-7c5e767cde12_20211013123456.png
    """
    file_name = (
        (remove_vietnamese_accents(input_str=object_name).replace(" ", "_").lower())
        + "_"
        + (user_id + "_")
        if user_id
        else "" + datetime.now().strftime("%Y%m%d%H%M%S") + "." + file_extension
    )
    file_path = os.path.join(bucket_name, file_name)

    return file_path
