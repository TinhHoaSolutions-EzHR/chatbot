from typing import Optional

from llama_index.core.storage.docstore.keyval_docstore import KVDocumentStore
from llama_index.core.storage.docstore.types import DEFAULT_BATCH_SIZE
from sqlalchemy.orm import Session

from app.integrations.llama_index.kvstore.mssql import MSSQLKVStore


class MSSQLDocumentStore(KVDocumentStore):
    """
    SQL Server implementation of the Document Store.
    An SQL Server store for Document and Node objects.
    """

    def __init__(
        self,
        mssql_kvstore: MSSQLKVStore,
        namespace: Optional[str] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ):
        """
        Initialize the SQL Server Document Store.

        Args:
            mssql_kvstore (MSSQLKVStore): The SQL Server Key-Value Store.
            namespace (str): The namespace to use for the Document Store. Defaults to None.
            batch_size (int): The batch size to use for the Document Store. Defaults to 1.
        """
        super().__init__(kvstore=mssql_kvstore, namespace=namespace, batch_size=batch_size)

    @classmethod
    def from_uri(
        cls,
        uri: str,
        namespace: Optional[str] = None,
        table_name: str = "docstore",
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MSSQLDocumentStore":
        """
        Initialize the SQL Server Document Store from a URI.

        Args:
            uri (str): The URI to connect to the SQL Server.
            namespace (str): The namespace to use for the Document Store. Defaults to None.
            table_name (str): The table name to use for the Document Store. Defaults to "docstore".
            perform_setup (bool): Whether to perform the setup of the Document Store. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.

        Returns:
            MSSQLDocumentStore: The SQL Server Document Store.
        """
        mssql_kvstore = MSSQLKVStore.from_uri(
            uri=uri, table_name=table_name, perform_setup=perform_setup, debug=debug
        )
        return cls(mssql_kvstore, namespace)

    @classmethod
    def from_params(
        cls,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        namespace: Optional[str] = None,
        table_name: str = "docstore",
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MSSQLDocumentStore":
        """
        Initialize the SQL Server Document Store from parameters.

        Args:
            host (str): The host to connect to the SQL Server.
            port (int): The port to connect to the SQL Server.
            database (str): The database to use for the SQL Server.
            user (str): The user to use for the SQL Server.
            password (str): The password to use for the SQL Server.
            namespace (str): The namespace to use for the Document Store. Defaults to None.
            table_name (str): The table name to use for the Document Store. Defaults to "docstore".
            perform_setup (bool): Whether to perform the setup of the Document Store. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.

        Returns:
            MSSQLDocumentStore: The SQL Server Document Store.
        """
        mssql_kvstore = MSSQLKVStore.from_params(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            table_name=table_name,
            perform_setup=perform_setup,
            debug=debug,
        )
        return cls(mssql_kvstore, namespace)

    @classmethod
    def from_session(
        cls,
        session: Session,
        namespace: Optional[str] = None,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MSSQLDocumentStore":
        """
        Initialize the SQL Server Document Store from a session.

        Args:
            session (Session): The session to use for the SQL Server.
            namespace (str): The namespace to use for the Document Store. Defaults to None.
            perform_setup (bool): Whether to perform the setup of the Document Store. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.

        Returns:
            MSSQLDocumentStore: The SQL Server Document Store.
        """
        mssql_kvstore = MSSQLKVStore.from_session(
            session=session, perform_setup=perform_setup, debug=debug
        )
        return cls(mssql_kvstore, namespace)
