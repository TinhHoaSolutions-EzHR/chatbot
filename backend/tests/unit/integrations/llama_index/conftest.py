import time
from collections.abc import Generator
from typing import Dict
from typing import Union

import docker
import pytest
from docker.models.containers import Container

from app.integrations.llama_index.kvstore.mssql import MSSQLKVStore


class ContainerStartError(Exception):
    """
    Custom exception raised when a container fails to start.
    """


@pytest.fixture
def mssql_container() -> Generator[Dict[str, Union[str, Container]], None, None]:
    """
    Pytest fixture that starts a MSSQL container and returns the container object.

    Returns:
        Generator[Dict[str, Union[str, Container]], None, None]: A dictionary containing the container name and the container object.
    """
    # Configure MSSQL parameters
    DB_NAME = "master"
    SA_PASSWORD = "P&ssword123"

    container = None
    try:
        # Initialize the Docker client
        client = docker.from_env()

        # Start MSSQL container
        container = client.containers.run(
            image="mcr.microsoft.com/mssql/server:2019-CU29-GDR1-ubuntu-20.04",
            environment={
                "ACCEPT_EULA": "Y",
                "MSSQL_SA_PASSWORD": SA_PASSWORD,
                "MSSQL_PID": "Express",
            },
            ports={"1433/tcp": 1434},
            detach=True,
        )

        # Retrieve the container's port
        container.reload()
        host_port = container.attrs["NetworkSettings"]["Ports"]["1433/tcp"][0]["HostPort"]

        # Wait for MSSQL to start
        time.sleep(15)

        # Create connection string
        connection_string = f"mssql+pyodbc://sa:{SA_PASSWORD}@127.0.0.1:{host_port}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
        async_connection_string = f"mssql+aioodbc://sa:{SA_PASSWORD}@127.0.0.1:{host_port}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"

        # Yield container info
        yield {
            "container": container,
            "connection_string": connection_string,
            "async_connection_string": async_connection_string,
        }

    except Exception as e:
        # Raise custom exception
        raise ContainerStartError(f"Failed to start container: {e}")

    finally:
        # Clean up
        if container:
            container.stop()
            container.remove()
            client.close()


@pytest.fixture
def mssql_kvstore(
    mssql_container: Dict[str, Union[str, Container]],
) -> Generator[MSSQLKVStore, None, None]:
    """
    Pytest fixture that initializes an MSSQLKVStore object.

    Args:
        mssql_container (Dict[str, Union[str, Container]]): A dictionary containing the container name and the container object.

    Returns:
        Generator[MSSQLKVStore, None, None]: A generator that yields an MSSQLKVStore.
    """
    kvstore = None
    try:
        kvstore = MSSQLKVStore(
            connection_string=mssql_container["connection_string"],
            async_connection_string=mssql_container["async_connection_string"],
            table_name="test_kvstore",
        )
        yield kvstore
    finally:
        if kvstore:
            # Get all keys and delete them
            keys = kvstore.get_all().keys()
            for key in keys:
                kvstore.delete(key)
