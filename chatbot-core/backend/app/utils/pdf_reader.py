from typing import Annotated
from typing import List

import pdfplumber
from fastapi import File
from fastapi import UploadFile
from llama_index.core import Document

from app.utils.logger import LoggerFactory

logger = LoggerFactory().get_logger(__name__)


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
        logger.error(f"Failed to parse PDF file: {e}", exc_info=True)
        return None

    return documents
