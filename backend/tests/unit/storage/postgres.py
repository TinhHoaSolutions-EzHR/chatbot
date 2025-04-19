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
def postgres_engine() -> Iterator[Engine]:
    """
    Create PostgreSQL database engine
    """
    # Validate the PostgreSQL connection configuration
    validate_config(
        o=Secrets, required=["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT"]
    )
    validate_config(
        o=Constants,
        required=[
            "POSTGRES_CONNECTOR_URI",
            "POSTGRES_TEST_DB_NAME",
            "POSTGRES_DRIVER",
            "POSTGRES_POOL_SIZE",
            "POSTGRES_MAX_OVERFLOW",
            "POSTGRES_POOL_TIMEOUT",
            "POSTGRES_POOL_RECYCLE",
        ],
    )

    # Create POSTGRES engine
    uri = Constants.POSTGRES_CONNECTOR_URI.format(
        user=Secrets.POSTGRES_USER,
        password=Secrets.POSTGRES_SA_PASSWORD,
        host=Secrets.POSTGRES_HOST,
        port=Secrets.POSTGRES_PORT,
        db_name=Constants.POSTGRES_TEST_DB_NAME,
    )
    engine = create_engine(
        uri,
        pool_size=Constants.DATABASE_POOL_SIZE,
        max_overflow=Constants.DATABASE_MAX_OVERFLOW,
        pool_timeout=Constants.DATABASE_POOL_TIMEOUT,
        pool_recycle=Constants.DATABASE_POOL_RECYCLE,
    )
    yield engine
    engine.dispose()


def test_postgres_connection(postgres_engine: Engine) -> None:
    """
    Test if the PostgreSQL database is reachable by executing a simple query.

    Args:
        postgres_engine (Engine): POSTGRES engine
    """
    try:
        # Execute a simple query to check if the server is accessible
        with postgres_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            value = result.fetchone()[0]
            result.close()
            assert 1 == value, f"Expected query result to be 1, but got {value}."
    except OperationalError as e:
        pytest.fail(f"SQLAlchemy error while connecting to POSTGRES: {e}.")
    except Exception as e:
        pytest.fail(f"Unexpected error while connecting to POSTGRES: {e}.")
