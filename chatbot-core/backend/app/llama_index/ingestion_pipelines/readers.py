from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from markitdown import MarkItDown
from openai import OpenAI
from tenacity import retry
from tenacity import stop_after_delay

from app.settings.constants import Constants
from app.utils.api.helpers import get_logger
from app.utils.llm.helpers import get_openai_api_key

logger = get_logger(__name__)


class MarkitdownReader(BaseReader):
    """ """

    def __init__(self) -> None:
        self.openai_client = OpenAI(api_key=get_openai_api_key())
        self.md = MarkItDown(mlm_client=self.openai_client, mlm_model=Constants.LLM_MODEL)

    @retry(stop=stop_after_delay(Constants.RETRY_TIMES))
    def load_data(self, file: str | Path, extra_info: Optional[Dict] = None) -> List[Document]:
        """ """
        logger.info(f"Reading content from file: {file}")
        try:
            content = self.md.convert(file)
            text_content = content.text_content
        except Exception as e:
            logger.exception(f"Failed to convert markdown file: {e}")

        documents = []

        metadata = {"file_name": content.title}
        if extra_info:
            metadata.update(extra_info)

        documents.append(Document(text=text_content, metadata=metadata))

        return documents
