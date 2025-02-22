from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError

from app.settings import Constants
from app.settings import Secrets
from tests.utils import validate_config


@pytest.fixture
def mssql_engine() -> Iterator[Engine]:
    """
    Create MSSQL engine
    """
    # Validate the MSSQL connection configuration
    validate_config(
        o=Secrets, required=["MSSQL_USER", "MSSQL_SA_PASSWORD", "MSSQL_HOST", "MSSQL_PORT"]
    )
    validate_config(
        o=Constants,
        required=[
            "MSSQL_CONNECTOR_URI",
            "MSSQL_TEST_DB_NAME",
            "MSSQL_DRIVER",
            "MSSQL_POOL_SIZE",
            "MSSQL_MAX_OVERFLOW",
            "MSSQL_POOL_TIMEOUT",
            "MSSQL_POOL_RECYCLE",
        ],
    )

    # Create MSSQL engine
    uri = Constants.MSSQL_CONNECTOR_URI.format(
        user=Secrets.MSSQL_USER,
        password=Secrets.MSSQL_SA_PASSWORD,
        host=Secrets.MSSQL_HOST,
        port=Secrets.MSSQL_PORT,
        db_name=Constants.MSSQL_TEST_DB_NAME,
        driver=Constants.MSSQL_DRIVER,
    )
    engine = create_engine(
        uri,
        pool_size=Constants.MSSQL_POOL_SIZE,
        max_overflow=Constants.MSSQL_MAX_OVERFLOW,
        pool_timeout=Constants.MSSQL_POOL_TIMEOUT,
        pool_recycle=Constants.MSSQL_POOL_RECYCLE,
    )
    yield engine
    engine.dispose()


def test_mssql_connection(mssql_engine: Engine) -> None:
    """
    Test if the MSSQL server is reachable by executing a simple query.

    Args:
        mssql_engine (Engine): MSSQL engine
    """
    try:
        # Execute a simple query to check if the server is accessible
        with mssql_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            value = result.fetchone()[0]
            result.close()
            assert 1 == value, f"Expected query result to be 1, but got {value}."
    except OperationalError as e:
        pytest.fail(f"SQLAlchemy error while connecting to MSSQL: {e}.")
    except Exception as e:
        pytest.fail(f"Unexpected error while connecting to MSSQL: {e}.")
