import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from llama_index.core.storage.kvstore.types import BaseKVStore
from llama_index.core.storage.kvstore.types import DEFAULT_BATCH_SIZE
from llama_index.core.storage.kvstore.types import DEFAULT_COLLECTION
from sqlalchemy import create_engine
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.integrations.llama_index.kvstore.mssql.utils import extract_params_from_uri
from app.integrations.llama_index.kvstore.mssql.utils import get_data_model
from app.settings import Constants


class MSSQLKVStore(BaseKVStore):
    """
    SQL Server Implementation of the Key-Value Store
    """

    def __init__(
        self,
        connection_string: str,
        async_connection_string: str,
        table_name: str,
        perform_setup: bool = True,
        debug: bool = False,
    ):
        """
        Initialize the SQL Server Key-Value Store.

        Args:
            connection_string (str): The connection string for the database.
            async_connection_string (str): The async connection string for the database.
            table_name (str): The name of the table to store the key-value pairs.
            perform_setup (bool): Whether to create the table on initialization. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.
        """
        try:
            import pyodbc  # noqa
            import aioodbc  # noqa
            import sqlalchemy
            import sqlalchemy.ext.asyncio  # noqa
        except ImportError:
            raise ImportError(
                "`sqlalchemy[asyncio]`, `pyodbc` and `aioodbc` packages should be pre installed"
            )

        table_name = table_name.lower()
        self.connection_string = connection_string
        self.async_connection_string = async_connection_string
        self.table_name = table_name
        self.perform_setup = perform_setup
        self.debug = debug
        self._is_initialized = False

        # SQLAlchemy model
        self._base = declarative_base()
        self._table_class = get_data_model(
            base=self._base,
            table_name=table_name,
        )

    @classmethod
    def from_params(
        cls,
        host: Optional[str] = None,
        port: int = 1433,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        table_name: str = "kvstore",
        connection_string: Optional[str] = None,
        async_connection_string: Optional[str] = None,
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MSSQLKVStore":
        """
        Initialize the SQL Server Key-Value Store from parameters.

        Args:
            host (Optional[str]): The host of the database. Defaults to None.
            port (int): The port of the database. Defaults to 1433.
            database (Optional[str]): The name of the database. Defaults to None.
            user (Optional[str]): The username for the database. Defaults to None.
            password (Optional[str]): The password for the database. Defaults to None.
            table_name (str): The name of the table to store the key-value pairs. Defaults to "kvstore".
            connection_string (Optional[str]): The connection string for the database. Defaults to None.
            async_connection_string (Optional[str]): The async connection string for the database. Defaults to None.
            perform_setup (bool): Whether to create the table on initialization. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.

        Returns:
            MSSQLKVStore: The key-value store instance.
        """
        conn_str = connection_string or Constants.MSSQL_CONNECTOR_URI.format(
            user=user,
            password=password,
            host=host,
            port=port,
            db_name=database,
            driver=Constants.MSSQL_DRIVER,
        )
        async_conn_str = async_connection_string or Constants.MSSQL_ASYNC_CONNECTOR_URI.format(
            user=user,
            password=password,
            host=host,
            port=port,
            db_name=database,
            driver=Constants.MSSQL_DRIVER,
        )

        return cls(
            connection_string=conn_str,
            async_connection_string=async_conn_str,
            table_name=table_name,
            perform_setup=perform_setup,
            debug=debug,
        )

    @classmethod
    def from_uri(
        cls,
        uri: str,
        table_name: str = "kvstore",
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MSSQLKVStore":
        """
        Initialize the SQL Server Key-Value Store from a URI.

        Args:
            uri (str): The URI for the database.
            table_name (str): The name of the table to store the key-value pairs. Defaults to "kvstore".
            perform_setup (bool): Whether to create the table on initialization. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.

        Returns:
            MSSQLKVStore: The key-value store instance.
        """
        params = extract_params_from_uri(uri=uri)
        return cls.from_params(
            **params,
            table_name=table_name,
            perform_setup=perform_setup,
            debug=debug,
        )

    @classmethod
    def from_session(
        cls,
        session: Session | AsyncSession,
        table_name: str = "kvstore",
        perform_setup: bool = True,
        debug: bool = False,
    ) -> "MSSQLKVStore":
        """
        Return connection string from database session.

        Args:
            session (Session | AsyncSession): The database session.
            table_name (str): The name of the table to store the key-value pairs. Defaults to "kvstore".
            perform_setup (bool): Whether to create the table on initialization. Defaults to True.
            debug (bool): Whether to print debug information. Defaults to False.

        Returns:
            MSSQLKVStore: The key-value store instance.
        """
        params = extract_params_from_uri(uri=session.bind.url.render_as_string(hide_password=False))
        return cls.from_params(
            **params,
            table_name=table_name,
            perform_setup=perform_setup,
            debug=debug,
        )

    def _connect(self) -> None:
        """
        Make a connection to the database.
        """

        # Create the database engine and session
        self._engine = create_engine(url=self.connection_string, echo=self.debug)
        self._session = sessionmaker(bind=self._engine)

        # Create the async database engine and session
        self._async_engine = create_async_engine(url=self.async_connection_string)
        self._async_session = sessionmaker(bind=self._async_engine, class_=AsyncSession)

    def _create_tables_if_not_exists(self) -> None:
        """
        Create the table for storing key-value pairs if it does not already exist.
        """
        with self._session() as session, session.begin():
            self._base.metadata.create_all(session.connection())

    def _initialize(self) -> None:
        """
        Initialize the connection to the database.
        """
        if not self._is_initialized:
            self._connect()
            if self.perform_setup:
                self._create_tables_if_not_exists()
            self._is_initialized = True

    def put(
        self,
        key: str,
        val: Dict[str, Any],
        collection: str = DEFAULT_COLLECTION,
    ) -> None:
        """
        Put the value for the given key into the store.

        Args:
            key(str): The key to store the value under.
            val(Dict[str, Any]): The value to store.
            collection(str): The collection to store the value under. Defaults to "data".
        """
        self.put_all(kv_pairs=[(key, val)], collection=collection)

    async def aput(
        self,
        key: str,
        val: Dict[str, Any],
        collection: str = DEFAULT_COLLECTION,
    ) -> None:
        """
        Asynchronously put the value for the given key into the store.

        Args:
            key(str): The key to store the value under.
            val(Dict[str, Any]): The value to store.
            collection(str): The collection to store the value under. Defaults to "data".
        """
        await self.aput_all(kv_pairs=[(key, val)], collection=collection)

    def put_all(
        self,
        kv_pairs: List[Tuple[str, Dict[str, Any]]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        """
        Put multiple key-value pairs into the store.

        Args:
            kv_pairs(List[Tuple[str, Dict[str, Any]]]): The key-value pairs to store.
            collection(str): The collection to store the values under. Defaults to "data".
            batch_size(int): The number of key-value pairs to store in a single batch. Defaults to 1.
        """
        self._initialize()
        with self._session() as session:
            for i in range(0, len(kv_pairs), batch_size):
                batch = kv_pairs[i : i + batch_size]

                # Prepare the VALUES part of the SQL statement
                values_clause = ", ".join(
                    f"(:key_{i}, :namespace_{i}, :value_{i})" for i, _ in enumerate(batch)
                )

                # Prepare the raw SQL for bulk upsert
                stmt = text(
                    f"""
                    MERGE INTO {self._table_class.__tablename__} AS target
                    USING (VALUES {values_clause}) AS source ([key], [namespace], [value])
                    ON target.[key] = source.[key] AND target.[namespace] = source.[namespace]
                    WHEN MATCHED THEN
                        UPDATE SET target.[value] = source.[value]
                    WHEN NOT MATCHED THEN
                        INSERT ([key], [namespace], [value])
                        VALUES (source.[key], source.[namespace], source.[value]);
                    """
                )

                # Flatten the list of tuples for execute parameters
                params = {}
                for i, (key, value) in enumerate(batch):
                    params[f"key_{i}"] = key
                    params[f"namespace_{i}"] = collection
                    params[f"value_{i}"] = json.dumps(value)

                # Execute the bulk upsert
                session.execute(statement=stmt, params=params)
                session.commit()

    async def aput_all(
        self,
        kv_pairs: List[Tuple[str, Dict[str, Any]]],
        collection: str = DEFAULT_COLLECTION,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ) -> None:
        """
        Asynchronously put multiple key-value pairs into the store.

        Args:
            kv_pairs(List[Tuple[str, Dict[str, Any]]]): The key-value pairs to store.
            collection(str): The collection to store the values under. Defaults to "data".
            batch_size(int): The number of key-value pairs to store in a single batch. Defaults to 1.
        """
        self._initialize()
        async with self._async_session() as session:
            for i in range(0, len(kv_pairs), batch_size):
                batch = kv_pairs[i : i + batch_size]

                # Prepare the VALUES part of the SQL statement
                values_clause = ", ".join(
                    f"(:key_{i}, :namespace_{i}, :value_{i})" for i, _ in enumerate(batch)
                )

                # Prepare the raw SQL for bulk upsert
                stmt = text(
                    f"""
                    MERGE INTO {self._table_class.__tablename__} AS target
                    USING (VALUES {values_clause}) AS source ([key], [namespace], [value])
                    ON target.[key] = source.[key] AND target.[namespace] = source.[namespace]
                    WHEN MATCHED THEN
                        UPDATE SET target.[value] = source.[value]
                    WHEN NOT MATCHED THEN
                        INSERT ([key], [namespace], [value])
                        VALUES (source.[key], source.[namespace], source.[value]);
                    """
                )

                # Flatten the list of tuples for execute parameters
                params = {}
                for i, (key, value) in enumerate(batch):
                    params[f"key_{i}"] = key
                    params[f"namespace_{i}"] = collection
                    params[f"value_{i}"] = json.dumps(value)

                # Execute the bulk upsert
                await session.execute(statement=stmt, params=params)
                await session.commit()

    def get(self, key: str, collection: str = DEFAULT_COLLECTION) -> Optional[Dict[str, Any]]:
        """
        Get the value for the given key from the store.

        Args:
            key(str): The key to retrieve the value for.
            collection(str): The collection to retrieve the value from. Defaults to "data".

        Returns:
            Optional[Dict[str, Any]]: The value for the given key, if it exists.
        """
        self._initialize()
        with self._session() as session:
            result = session.execute(
                select(self._table_class).filter_by(key=key, namespace=collection)
            ).scalar()
            if result:
                return json.loads(result.value)

        return None

    async def aget(
        self, key: str, collection: str = DEFAULT_COLLECTION
    ) -> Optional[Dict[str, Any]]:
        """
        Asynchronously get the value for the given key from the store.

        Args:
            key(str): The key to retrieve the value for.
            collection(str): The collection to retrieve the value from. Defaults to "data".

        Returns:
            Optional[Dict[str, Any]]: The value for the given key, if it exists.
        """
        self._initialize()
        async with self._async_session() as session:
            result = await session.execute(
                select(self._table_class).filter_by(key=key, namespace=collection)
            )
            result = result.scalars().first()

        return json.loads(result.value) if result else None

    def get_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, Dict[str, Any]]:
        """
        Get all key-value pairs from the store.

        Args:
            collection(str): The collection to retrieve the values from. Defaults to "data".

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary of key-value pairs.
        """
        self._initialize()
        with self._session() as session:
            results = session.execute(select(self._table_class).filter_by(namespace=collection))
            results = results.scalars().all()

            return {result.key: json.loads(result.value) for result in results} if results else {}

    async def aget_all(self, collection: str = DEFAULT_COLLECTION) -> Dict[str, Dict[str, Any]]:
        """
        Asynchronously get all key-value pairs from the store.

        Args:
            collection(str): The collection to retrieve the values from. Defaults to "data".

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary of key-value pairs.
        """
        self._initialize()
        async with self._async_session() as session:
            results = await session.execute(
                select(self._table_class).filter_by(namespace=collection)
            )
            results = results.scalars().all()

        return {result.key: result.value for result in results} if results else {}

    def delete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
        """
        Delete the value for the given key from the store.

        Args:
            key(str): The key to delete the value for.
            collection(str): The collection to delete the value from. Defaults to "data".

        Returns:
            bool: True if the key was deleted, False otherwise
        """

        self._initialize()
        with self._session() as session:
            result = session.execute(
                delete(self._table_class).filter_by(key=key, namespace=collection)
            )
            session.commit()

        return result.rowcount > 0

    async def adelete(self, key: str, collection: str = DEFAULT_COLLECTION) -> bool:
        """
        Asynchronously delete the value for the given key from the store.

        Args:
            key(str): The key to delete the value for.
            collection(str): The collection to delete the value from. Defaults to "data".

        Returns:
            bool: True if the key was deleted, False otherwise
        """
        self._initialize()
        async with self._async_session() as session:
            result = await session.execute(
                delete(self._table_class).filter_by(key=key, namespace=collection)
            )
            await session.commit()

        return result.rowcount > 0
