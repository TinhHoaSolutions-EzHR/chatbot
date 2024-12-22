import logging
import os
import sys
from typing import Annotated
from typing import List

import pdfplumber
from fastapi import File
from fastapi import UploadFile
from llama_index.core import Document

from app.settings import Constants
from app.settings import Secrets
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


def get_database_url() -> str:
    """
    Get the database URL.

    Returns:
        str: Database URL.

    Example:
        >>> get_database_url()
        'mssql+pyodbc://sa:password@localhost/db_name?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Try create the database URL from the environment variables
        database_url = Constants.MSSQL_CONNECTOR_URI.format(
            user=Secrets.MSSQL_USER,
            password=Secrets.MSSQL_SA_PASSWORD,
            host=Secrets.MSSQL_HOST,
            db_name=Secrets.MSSQL_DB,
            driver=Constants.MSSQL_DRIVER,
        )

    return database_url
