from typing import Dict
from typing import Union

import pytest
from docker.models.containers import Container

from app.integrations.llama_index.kvstore.mssql import MSSQLKVStore

try:
    import aioodbc  # noqa
    import pyodbc  # noqa
    import sqlalchemy  # noqa

    no_packages = False
except ImportError:
    no_packages = True


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_kvstore_basic(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the basic functionality of the MSSQLKVStore class.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key = "test_key_basic"
    test_blob = {"test_obj_key": "test_obj_value"}
    mssql_kvstore.put(key=test_key, val=test_blob)
    blob = mssql_kvstore.get(key=test_key)
    assert blob == test_blob

    blob = mssql_kvstore.get(key=test_key, collection="non_existent_collection")
    assert blob is None

    deleted = mssql_kvstore.delete(key=test_key)
    assert deleted


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
@pytest.mark.asyncio
async def test_kvstore_async_basic(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the basic functionality of the MSSQLKVStore class with async methods.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key = "test_key_basic"
    test_blob = {"test_obj_key": "test_obj_value"}
    await mssql_kvstore.aput(key=test_key, val=test_blob)
    blob = await mssql_kvstore.aget(key=test_key)
    assert blob == test_blob

    blob = await mssql_kvstore.aget(key=test_key, collection="non_existent_collection")
    assert blob is None

    deleted = await mssql_kvstore.adelete(key=test_key)
    assert deleted


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_kvstore_getall(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the get_all method of the MSSQLKVStore class.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key_1 = "test_key_1"
    test_blob_1 = {"test_obj_key": "test_obj_value"}
    mssql_kvstore.put(key=test_key_1, val=test_blob_1)
    blob = mssql_kvstore.get(key=test_key_1)
    assert blob == test_blob_1

    test_key_2 = "test_key_2"
    test_blob_2 = {"test_obj_key": "test_obj_value"}
    mssql_kvstore.put(key=test_key_2, val=test_blob_2)
    blob = mssql_kvstore.get(key=test_key_2)
    assert blob == test_blob_2

    blob = mssql_kvstore.get_all()
    assert len(list(blob.keys())) == 2

    mssql_kvstore.delete(key=test_key_1)
    mssql_kvstore.delete(key=test_key_2)


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
@pytest.mark.asyncio
async def test_kvstore_agetall(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the aget_all method of the MSSQLKVStore class.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key_1 = "test_key_1"
    test_blob_1 = {"test_obj_key": "test_obj_value"}
    await mssql_kvstore.aput(key=test_key_1, val=test_blob_1)
    blob = await mssql_kvstore.aget(key=test_key_1)
    assert blob == test_blob_1

    test_key_2 = "test_key_2"
    test_blob_2 = {"test_obj_key": "test_obj_value"}
    await mssql_kvstore.aput(key=test_key_2, val=test_blob_2)
    blob = await mssql_kvstore.aget(key=test_key_2)
    assert blob == test_blob_2

    blobs = await mssql_kvstore.aget_all()
    assert len(blobs) == 2

    await mssql_kvstore.adelete(key=test_key_1)
    await mssql_kvstore.adelete(key=test_key_2)


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
@pytest.mark.asyncio
async def test_kvstore_aputall(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the aput_all method of the MSSQLKVStore class.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key1 = "test_key_putall_1"
    test_blob1 = {"test_obj_key": "test_obj_value"}
    test_key_2 = "test_key_putall_2"
    test_blob_2 = {"test_obj_key": "test_obj_value"}
    await mssql_kvstore.aput_all(kv_pairs=[(test_key1, test_blob1), (test_key_2, test_blob_2)])
    blob = await mssql_kvstore.aget(key=test_key1)
    assert blob == test_blob1
    blob = await mssql_kvstore.aget(key=test_key_2)
    assert blob == test_blob_2

    await mssql_kvstore.adelete(key=test_key1)
    await mssql_kvstore.adelete(key=test_key_2)


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_kvstore_delete(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the delete method of the MSSQLKVStore class.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key = "test_key_delete"
    test_blob = {"test_obj_key": "test_obj_value"}
    mssql_kvstore.put(key=test_key, val=test_blob)
    blob = mssql_kvstore.get(key=test_key)
    assert blob == test_blob

    mssql_kvstore.delete(key=test_key)
    blob = mssql_kvstore.get(key=test_key)
    assert blob is None


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
@pytest.mark.asyncio
async def test_kvstore_adelete(mssql_kvstore: MSSQLKVStore) -> None:
    """
    Test the adelete method of the MSSQLKVStore class.

    Args:
        mssql_kvstore (MSSQLKVStore): An MSSQLKVStore object.
    """
    test_key = "test_key_delete"
    test_blob = {"test_obj_key": "test_obj_value"}
    await mssql_kvstore.aput(key=test_key, val=test_blob)
    blob = await mssql_kvstore.aget(key=test_key)
    assert blob == test_blob

    await mssql_kvstore.adelete(key=test_key)
    blob = await mssql_kvstore.aget(key=test_key)
    assert blob is None


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_from_uri(
    mssql_container: Dict[str, Union[str, Container]],
) -> None:
    """
    Test the MSSQLKVStore.from_uri() method.

    Args:
        mssql_container (Dict[str, Union[str, Container]]): A dictionary containing the container name and the container object.
    """
    kvstore = MSSQLKVStore.from_uri(
        uri=mssql_container["connection_string"],
    )
    output = kvstore.get_all()
    assert len(list(output.keys())) == 0


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
def test_from_session(
    mssql_container: Dict[str, Union[str, Container]],
) -> None:
    """
    Test the MSSQLKVStore.from_session() method.

    Args:
        mssql_container (Dict[str, Union[str, Container]]): A dictionary containing the container name and the container object.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(mssql_container["connection_string"])
    session = sessionmaker(bind=engine)

    kvstore = MSSQLKVStore.from_session(session=session())
    output = kvstore.get_all()
    assert len(list(output.keys())) == 0


@pytest.mark.skipif(
    no_packages,
    reason="aioodbc, pyodbc, and sqlalchemy are required for this test",
)
@pytest.mark.asyncio
async def test_from_async_session(
    mssql_container: Dict[str, Union[str, Container]],
) -> None:
    """
    Test the MSSQLKVStore.from_async_session() method.

    Args:
        mssql_container (Dict[str, Union[str, Container]]): A dictionary containing the container name and the container object.
    """
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    async_engine = create_async_engine(mssql_container["async_connection_string"])
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession)

    kvstore = MSSQLKVStore.from_session(session=async_session())
    output = await kvstore.aget_all()
    assert len(list(output.keys())) == 0
