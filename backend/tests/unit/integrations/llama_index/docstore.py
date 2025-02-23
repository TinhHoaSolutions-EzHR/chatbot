from typing import List

import pytest
from llama_index.core.schema import BaseNode
from llama_index.core.schema import Document

from app.integrations.llama_index.docstore.mssql import MSSQLDocumentStore
from app.integrations.llama_index.kvstore.mssql import MSSQLKVStore

try:
    import aioodbc  # noqa
    import pyodbc  # noqa
    import sqlalchemy  # noqa

    no_packages = False
except ImportError:
    no_packages = True


@pytest.fixture
def documents() -> List[Document]:
    """
    Pytest fixture that initializes a list of documents.

    Returns:
        List[Document]: A list of documents.
    """
    return [
        Document(text="doc_1"),
        Document(text="doc_2"),
    ]


@pytest.fixture
def mssql_docstore(mssql_kvstore: MSSQLKVStore) -> MSSQLDocumentStore:
    """
    Pytest fixture that initializes an MSSQLDocumentStore object.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.

    Returns:
        MSSQLDocumentStore: An MSSQLDocumentStore object.
    """
    return MSSQLDocumentStore(mssql_kvstore=mssql_kvstore)


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_mssql_docstore(
    mssql_docstore: MSSQLDocumentStore,
    documents: List[Document],
) -> None:
    """
    Test the basic functionality of the MSSQLDocumentStore class.

    Args:
        mssql_docstore (MSSQLDocumentStore): An MSSQLDocumentStore object.
        documents (List[Document]): A list of documents.
    """
    ds = mssql_docstore
    assert len(ds.docs) == 0

    # Test adding documents
    ds.add_documents(docs=documents)
    assert len(ds.docs) == 2
    assert all(isinstance(doc, BaseNode) for doc in ds.docs.values())

    # Test updating documents
    ds.add_documents(docs=documents)
    assert len(ds.docs) == 2

    # Test getting documents
    doc0 = ds.get_document(doc_id=documents[0].get_doc_id())
    assert doc0 is not None
    assert documents[0].get_content() == doc0.get_content()

    # Test deleting documents
    ds.delete_document(documents[0].get_doc_id())
    assert len(ds.docs) == 1


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_mssql_docstore_hash(mssql_docstore: MSSQLDocumentStore) -> None:
    """
    Test the hashing functionality of the MSSQLDocumentStore class.

    Args:
        mssql_docstore (MSSQLDocumentStore): An MSSQLDocumentStore object.
    """
    ds = mssql_docstore

    # Test setting hash
    ds.set_document_hash("test_doc_id", "test_doc_hash")
    doc_hash = ds.get_document_hash("test_doc_id")
    assert doc_hash == "test_doc_hash"

    # Test updating hash
    ds.set_document_hash("test_doc_id", "test_doc_hash_new")
    doc_hash = ds.get_document_hash("test_doc_id")
    assert doc_hash == "test_doc_hash_new"

    # Test getting non-existent
    doc_hash = ds.get_document_hash("non_existent_doc_id")
    assert doc_hash is None
