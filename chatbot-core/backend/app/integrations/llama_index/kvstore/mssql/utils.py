from typing import Any
from typing import Dict
from typing import Type
from urllib.parse import urlparse


def get_data_model(base: Type, table_name: str) -> Type:
    """
    This function creates a dynamic SQLAlchemy model with a new table for MSSQL.

    Args:
        base (Type): The SQLAlchemy base class.
        table_name (str): The name of the table to create.

    Returns:
        Type: A new SQLAlchemy model class.
    """
    from sqlalchemy import Column, Integer, Index, UniqueConstraint, NVARCHAR

    tablename = f"data_{table_name}"
    class_name = f"Data{table_name.capitalize()}"

    class AbstractData(base):
        """
        Abstract base class for the data model.
        """

        __abstract__ = True

        id = Column(Integer, primary_key=True, autoincrement=True)
        key = Column(NVARCHAR(255), nullable=False)
        namespace = Column(NVARCHAR(255), nullable=False)
        value = Column(NVARCHAR(max), nullable=True)

    return type(
        class_name,
        (AbstractData,),
        {
            "__tablename__": tablename,
            "__table_args__": (
                UniqueConstraint("key", "namespace", name=f"{tablename}_unique_key_namespace"),
                Index(f"{tablename}_idx_key_namespace", "key", "namespace"),
            ),
        },
    )


def extract_params_from_uri(uri: str) -> Dict[str, Any]:
    """
    This function extracts the parameters from a URI.

    Args:
        uri (str): The URI to extract parameters from.

    Returns:
        Dict[str, Any]: A dictionary of parameters.
    """
    result = urlparse(uri=uri)
    database = result.path[1:]
    port = result.port if result.port else 1433
    return {
        "host": result.hostname,
        "port": port,
        "username": result.username,
        "password": result.password,
        "database": database,
    }