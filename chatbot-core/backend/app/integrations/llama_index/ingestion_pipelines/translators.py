import asyncio
from abc import ABC
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

from app.integrations.llama_index.prompts.translator import TRANSLATOR_PROMPT_TMPL
from app.utils.api.helpers import get_logger

logger = get_logger(__name__)


class Translator(ABC, BaseModel):
    """Base interface for all translators.

    Attributes:
        llm (BaseLLM): The LLM model used for translation.
        source_language (str): The source language of the text to be translated.
        target_language (str): The target language of the translated text.

    Public Methods:
        from_defaults: Create an instance using default settings.
        get_translated_documents: Translate a list of documents from source language to target language.
        translate_text: Translate a text from source language to target language.
    """

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
        """
        Initializes the translator with a language model, source and target languages, and a callback manager.

        Args:
            llm (BaseLLM): The language model to be used. If None, defaults to Settings.llm.
            source_language (str): The language code of the source text.
            target_language (str): The language code of the target text.
            callback_manager (CallbackManager): Manages callbacks during translation.
        """
        self.llm = llm or Settings.llm
        self.source_language = source_language
        self.target_language = target_language
        self.callback_manager = callback_manager

    @property
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
        """
        Create an instance using default settings.

         Args:
             llm (Optional[BaseLLM]): Language model. Defaults to Settings.llm if not provided.
             source_language (Optional[str]): Source language. Defaults to "vietnamese".
             target_language (Optional[str]): Target language. Defaults to "english".
             callback_manager (Optional[CallbackManager]): Callback manager for handling events. Defaults to an empty CallbackManager.

         Returns:
             An instance of the class with the provided or default parameters.
        """
        callback_manager = callback_manager or CallbackManager([])
        llm = llm or Settings.llm

        return cls(
            llm=llm,
            source_language=source_language,
            target_language=target_language,
            callback_manager=callback_manager,
        )

    async def _translate_chunk(cls, chunk: str) -> str:
        """Translate a chunk of text from source language to target language."""
        prompt = TRANSLATOR_PROMPT_TMPL.format(
            source_language=cls.source_language, target_language=cls.target_language, document=chunk
        )
        translated_text = await cls.llm.acomplete(prompt)

        return translated_text.text

    async def _translate_document(cls, document: Document, show_progress: bool = False) -> Document:
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
            *(cls._translate_chunk(chunk) for chunk in chunks_with_progress)
        )

        translated_text = "\n".join(translated_chunks)
        return Document(text=translated_text, metadata=document.metadata)

    def get_translated_documents(
        cls, documents: List[Document], show_progress: bool = False
    ) -> List[Document]:
        """Translate a list of documents from source language to target language.
        Default: English -> Vietnamese

        Args:
            documents (Sequence[Document]): List of documents to be translated.
            show_progress (bool): Flag to show progress bar. Defaults to False.

        Returns:
            List[Document]: List of translated documents.

        Examples:
            >>> get_translated_documents([Document(text="Hello, how are you?", metadata=metadata)])
            [Document(text="Xin chào, bạn có khỏe không?", metadata=metadata)]
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
                    translated_doc = asyncio.run(cls._translate_document(document, show_progress))
                    translated_documents.append(translated_doc)
                except Exception as e:
                    logger.error(f"Failed to translate document {document.id_}: {e}", exc_info=True)

            event.on_end({EventPayload.DOCUMENTS: translated_documents})

        return translated_documents

    def translate_text(cls, text: str) -> str:
        """Translate a text from source language to target language.

        Args:
            text (str): The text to be translated.

        Returns:
            str: The translated text.

        Examples:
            >>> translate_text("Hello, how are you?")
            "Xin chào, bạn có khỏe không?"
        """
        translated_result = asyncio.run(cls._translate_chunk(text))
        return translated_result
