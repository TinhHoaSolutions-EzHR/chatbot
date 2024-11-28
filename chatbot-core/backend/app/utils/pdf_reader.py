import pdfplumber
from fastapi import File, UploadFile
from llama_index.core import Document
from typing import Annotated, List

from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


def parse_pdf(
    file: Annotated[UploadFile, File(description="PDF file")],
) -> List[Document] | None:
    """
    Parse a PDF file into Llamaindex Document objects.

    Args:
        file (UploadFile): PDF file to parse.

    Returns:
        List[Document]: List of Llamaindex Document objects.
    """
    try:
        documents = []
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                documents.append(Document(text=page.extract_text()))
    except Exception as e:
        logger.error(f"Failed to parse PDF file: {e}")
        return None

    return documents
