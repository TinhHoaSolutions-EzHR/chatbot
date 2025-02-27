from typing import Dict
from typing import List
from typing import Optional

from llama_index.core import Settings
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from markitdown import MarkItDown
from tenacity import retry
from tenacity import stop_after_delay

from app.settings.constants import Constants
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class MarkitdownReader(BaseReader):
    """Reads content from a pdf file and returns a list of documents under markdown format."""

    def __init__(self) -> None:
        """Try to create an MarkItDown with OpenAI client, if not found, use default MarkItDown."""
        try:
            self.openai_client = Settings.llm
            self.md = MarkItDown(llm_client=self.openai_client, llm_model=Constants.LLM_MODEL)
        except Exception as e:
            logger.warning(f"Failed to create MarkItDown with OpenAI client: {e}")
            self.openai_client = None
            self.md = MarkItDown()

    @retry(stop=stop_after_delay(Constants.RETRY_TIMES))
    def load_data(self, file: str, extra_info: Optional[Dict] = None) -> List[Document]:
        """
        Load data from a pdf file and return a list of documents under markdown format.

        Args:
            file (str): The path to the pdf file.
            extra_info (Optional[Dict]): Extra information to be added to the metadata of the document.

        Returns:
            List[Document]: A list of documents under markdown format.

        Raises:
            Exception: If the file is not found or failed to convert the file
        """
        logger.info(f"Reading content from file: {file}")
        try:
            content = self.md.convert(file)
            text_content = content.text_content
        except Exception as e:
            logger.exception(f"Failed to convert markdown file: {e}")

        documents = []

        title = content.title or file.split("/")[-1]
        metadata = {"file_name": title}
        if extra_info:
            metadata.update(extra_info)

        documents.append(Document(text=text_content, metadata=metadata))

        return documents
