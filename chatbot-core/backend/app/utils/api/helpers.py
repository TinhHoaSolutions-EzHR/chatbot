import asyncio
import logging
import os
import sys
from collections.abc import Callable
from datetime import datetime
from typing import List

import pdfplumber
from fastapi import File
from fastapi import Request
from fastapi import UploadFile
from llama_index.core import Document

from app.settings import Constants
from app.settings import Secrets
from app.utils.api.error_handler import PdfParsingError

# TODO: Replace this logger by own logger after moving logger logic to separate module
logger = logging.getLogger(__name__)


def parse_pdf(
    document: UploadFile,
    issue_date: datetime = datetime.now(),
    is_outdated: bool = False,
) -> List[Document] | None:
    """
    Parse a PDF file into Llamaindex Document objects.

    Args:
        document (UploadFile): PDF file to parse.
        issue_date (datetime): Issue date of the document. Defaults to the current date.
        is_outdated (bool): Flag to indicate if the document is outdated. Defaults to False.

    Returns:
        List[Document]: List of Llamaindex Document objects.
    """
    try:
        documents = []
        with pdfplumber.open(document.file) as pdf:
            for page in pdf.pages:
                # Extract text from the page
                page_text = page.extract_text()
                if not page_text:
                    continue

                # Define metadata for the document
                metadata = {
                    "issue_date": issue_date.strftime(Constants.DATETIME_FORMAT),
                    "outdated": is_outdated,
                    "page_number": page.page_number,
                }

                # Create a Llamaindex Document object
                doc = Document(text=page_text, metadata=metadata)
                documents.append(doc)
    except Exception as e:
        raise PdfParsingError(message="Error parsing PDF", detail=str(e))

    return documents


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[1;31m",  # Bold Red
        "NOTSET": "\033[91m",  # Reset
        "NOTICE": "\033[94m",  # Blue
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            str: Formatted log message.
        """
        # Get the log level name
        levelname = record.levelname
        if levelname in self.COLORS:
            prefix = self.COLORS[levelname]
            suffix = "\033[0m"

            # Format the log message
            formatted_message = super().format(record)
            level_display = f"{prefix}{levelname}{suffix}:"
            return f"{level_display.ljust(18)} {formatted_message}"

        return super().format(record)


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

    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.handlers = []
    uvicorn_logger.setLevel(log_level)

    if not logger.hasHandlers():
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )

        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            if uvicorn_logger:
                uvicorn_logger.addHandler(console_handler)

        if log_to_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            if uvicorn_logger:
                uvicorn_logger.addHandler(console_handler)

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
            port=Secrets.MSSQL_PORT,
            db_name=Secrets.MSSQL_DB,
            driver=Constants.MSSQL_DRIVER,
        )

    return database_url


def check_client_disconnected(request: Request) -> Callable[[], bool]:
    """
    Check if the client is disconnected when streaming response.

    Args:
        request (Request): Request object.

    Returns:
        Callable[[], bool]: Function to check if the client is disconnected.
    """

    async def is_client_disconnected() -> bool:
        try:
            return await request.is_disconnected()
        except asyncio.TimeoutError:
            logger.warning("Timeout error while checking if the client is disconnected")
            return True
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while checking if the client is disconnected: {str(e)}"
            )
            return True

    return is_client_disconnected
