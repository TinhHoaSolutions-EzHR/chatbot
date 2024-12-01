from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")


class BaseConnector(ABC, Generic[T]):
    """
    Base connector class

    Pattern: Singleton
    Purpose: Generalize the connection logic for external services
    """

    _instance: Optional["BaseConnector[T]"] = None
    _client: Optional[T] = None
    _o: Optional[object] = None
    _required_keys: List[str] = []

    def __new__(cls, *args, **kwargs) -> "BaseConnector[T]":
        """
        Create a single instance of the connection

        Returns:
            BaseConnector[T]: Connection instance
        """
        if cls._instance is None:
            # Validate the connection configuration
            cls._validate_config(o=cls._o, required=cls._required_keys)

            # Create the connection instance & client
            cls._instance = super(BaseConnector, cls).__new__(cls)
            cls._instance._client = cls._create_client(*args, **kwargs)

        return cls._instance

    @property
    def client(self) -> T:
        """
        Get the client instance
        """
        if self._client is None:
            raise RuntimeError(f"{self.__class__.__name__}: Client is not initialized")

        return self._client

    @staticmethod
    def _validate_config(o: object, required: List[str]) -> None:
        """
        Validate connection configuration

        Args:
            o (object): The object to validate
            required (List[str]): The list of required attributes

        Raises:
            ValueError: If any of the required attributes are missing
        """
        for key in required:
            if not hasattr(o, key) or not getattr(o, key):
                raise ValueError(f"Missing required connection configuration: {key}")

    @classmethod
    @abstractmethod
    def _create_client(cls, *args, **kwargs) -> T:
        """
        Create the connection

        Returns:
            Any: connection instance
        """
        raise NotImplementedError