import hashlib
import logging
import os
import sys
from datetime import datetime
from io import BytesIO
from typing import Annotated
from typing import List

import pdfplumber
import pydenticon
from fastapi import File
from fastapi import UploadFile
from llama_index.core import Document

from app.settings import Constants
from app.utils.api.error_handler import PdfParsingError


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


def parse_pdf(
    document: Annotated[UploadFile, File(description="PDF file")],
) -> List[Document] | None:
    """
    Parse a PDF file into Llamaindex Document objects.

    Args:
        document (UploadFile): PDF file to parse.

    Returns:
        List[Document]: List of Llamaindex Document objects.
    """
    try:
        documents = []
        with pdfplumber.open(document.file) as pdf:
            for page in pdf.pages:
                documents.append(Document(text=page.extract_text()))
    except Exception as e:
        raise PdfParsingError(message="Error parsing PDF", detail=str(e))

    return documents


def get_logger(
    name: str,
    log_level: str | int = Constants.LOGGER_LOG_LEVEL,
    log_to_console: bool = Constants.LOGGER_LOG_TO_CONSOLE,
    log_to_file: bool = Constants.LOGGER_LOG_TO_FILE,
    log_file_path: str = Constants.LOGGER_LOG_FILE_PATH,
    max_bytes: int = Constants.LOGGER_MAX_BYTES,
    backup_count: int = Constants.LOGGER_BACKUP_COUNT,
) -> logging.Logger:
    """
    Get the logger instance

    Args:
        name (str): Name of the logger.
        log_level (str | int): Log level.
        log_to_console (bool): Log to console.
        log_to_file (bool): Log to file.
        log_file_path (str): Log file path.
        max_bytes (int): Max bytes.
        backup_count (int): Backup count.

    Returns:
        logging.Logger: Logger instance.
    """
    logger = logging.getLogger(name=name)
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        if log_to_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


def construct_file_path(object_name: str, user_id: str = None) -> str:
    """
    Construct file path in Minio.

    Args:
        object_name (str): Name of the object.
        user_id (str): User id. Defaults to None.

    Returns:
        str: File path in Minio.
    """
    file_name = (
        (remove_vietnamese_accents(input_str=object_name).replace(" ", "_").lower())
        + "_"
        + user_id
        + "_"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + ".png"
    )
    file_path = os.path.join(Constants.MINIO_IMAGE_BUCKET, file_name)

    return file_path


def generate_avatar_image(data: str) -> BytesIO:
    """
    Generate an avatar image.

    Args:
        data (str): Data to generate the avatar.

    Returns:
        BytesIO: Avatar image.
    """
    generator = pydenticon.Generator(
        rows=5,
        columns=5,
        digest=hashlib.sha1,
        foreground=Constants.AGENT_AVATAR_IDENTICON_FOREGROUND_COLOR,
        background=Constants.AGENT_AVATAR_IDENTICON_BACKGROUND_COLOR,
    )

    # Generate the image
    image_data = generator.generate(
        data=data,
        width=Constants.AGENT_AVATAR_IDENTICON_WIDTH,
        height=Constants.AGENT_AVATAR_IDENTICON_HEIGHT,
        output_format=Constants.AGENT_AVATAR_IDENTICON_OUTPUT_FORMAT,
    )

    # Convert to BinaryIO
    agent_avatar = BytesIO(image_data)

    return agent_avatar
