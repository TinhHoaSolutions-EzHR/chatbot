import asyncio
from abc import ABC
from typing import Any
from typing import List
from typing import Optional

from llama_index.core import Settings
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.callbacks import CallbackManager
from llama_index.core.callbacks import CBEventType
from llama_index.core.callbacks import EventPayload
from llama_index.core.schema import Document
from llama_index.core.utils import get_tqdm_iterable
from pydantic import BaseModel
from pydantic import Field
from pydantic import SerializeAsAny

from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class Translator(ABC, BaseModel):
    """Base interface for all translators."""

    llm: SerializeAsAny[BaseLLM] = Field(
        default=None,
        description="The LLM model used for translation.",
        exclude=True,
    )

    source_language: str = Field(
        default="vietnamese",
        description="The source language of the text to be translated.",
        exclude=True,
    )

    target_language: str = Field(
        default="english",
        description="The target language of the translated text.",
    )

    def __init__(
        self,
        llm: BaseLLM,
        source_language: str,
        target_language: str,
        callback_manager: CallbackManager,
    ) -> None:
        self.llm = llm or Settings.llm
        self.source_language = source_language
        self.target_language = target_language
        self.callback_manager = callback_manager

    @classmethod
    def class_name(cls):
        return cls.__name__

    @classmethod
    def from_defaults(
        cls,
        llm: Optional[BaseLLM] = None,
        source_language: Optional[str] = "vietnamese",
        target_language: Optional[str] = "english",
        callback_manager: Optional[CallbackManager] = None,
    ):
        callback_manager = callback_manager or CallbackManager([])
        llm = llm or Settings.llm

        return cls(
            llm=llm,
            source_language=source_language,
            target_language=target_language,
            callback_manager=callback_manager,
        )

    async def _translate_chunk(cls, chunk: str, **kwargs: Any) -> str:
        """Translate a chunk of text from source language to target language."""
        prompt_template = """\
            Translate the following documents from {source_language} to {target_language}:
            '''
            {document}
            '''
        """

        prompt = prompt_template.format(
            source_language=cls.source_language, target_language=cls.target_language, document=chunk
        )
        translated_text = await cls.llm.acomplete(prompt)

        return translated_text.text

    async def _translate_document(
        cls, document: Document, show_progress: bool = False, **kwargs: Any
    ) -> Document:
        """Translate a list of documents from source language to target language.
        Default: English -> Vietnamese

        Args:
            documents (Sequence[Document]): List of documents to be translated.
            show_progress (bool): Flag to show progress bar. Defaults to False.
        """

        # Split the document into chunks with a maximum length of 4096 tokens
        max_chunk_length = 4096
        original_text = document.text
        chunks = [
            original_text[i : i + max_chunk_length]
            for i in range(0, len(original_text), max_chunk_length)
        ]
        chunks_with_progress = get_tqdm_iterable(chunks, show_progress, "Translating chunks")

        translated_chunks = await asyncio.gather(
            *(cls._translate_chunk(chunk, **kwargs) for chunk in chunks_with_progress)
        )

        translated_text = "\n".join(translated_chunks)
        return Document(text=translated_text, metadata=document.metadata)

    def get_translated_documents(
        cls, documents: List[Document], show_progress: bool = False, **kwargs: Any
    ) -> List[Document]:
        """Translate a list of documents from source language to target language.
        Default: English -> Vietnamese

        Args:
            documents (Sequence[Document]): List of documents to be translated.
            show_progress (bool): Flag to show progress bar. Defaults to False.
        """
        translated_documents = []
        documents_with_progress = get_tqdm_iterable(
            documents, show_progress, "Translating documents"
        )

        with cls.callback_manager.event(
            CBEventType.CHUNKING, payload={EventPayload.DOCUMENTS: documents}
        ) as event:
            for document in documents_with_progress:
                try:
                    translated_doc = asyncio.run(
                        cls._translate_document(document, show_progress, **kwargs)
                    )
                    translated_documents.append(translated_doc)
                except Exception as e:
                    logger.error(f"Failed to translate document {document.id_}: {e}", exc_info=True)

            event.on_end({EventPayload.DOCUMENTS: translated_documents})

        return translated_documents

    def translate_text(cls, text: str, **kwargs: Any) -> str:
        """Translate a text from source language to target language."""
        translated_result = asyncio.run(cls._translate_chunk(text, **kwargs))
        return translated_result
