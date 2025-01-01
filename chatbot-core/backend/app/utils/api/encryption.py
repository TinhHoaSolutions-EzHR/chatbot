import threading
from typing import Optional

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from app.models import EncryptionKey
from app.repositories.encryption import EncryptionRepository
from app.utils.api.error_handler import DatabaseTransactionError


class SecretKeyManager:
    """
    SecretKeyManager class for handling API key-related operations.
    Implements a thread-safe singleton pattern for managing encryption keys.
    """

    _instance = None
    _lock = threading.Lock()  # For thread-safe singleton initialization
    _encryption_key: Optional[bytes] = None
    _cipher_suite: Optional[Fernet] = None

    def __new__(cls, db_session: Session) -> "SecretKeyManager":
        """
        Ensure single instance creation (Singleton pattern).
        Thread-safe implementation using a lock.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_session: Session):
        """
        Initialize SecretKeyManager with database session and encryption setup.

        Args:
            db_session (Session): SQLAlchemy database session

        Raises:
            DatabaseTransactionError: If encryption key operations fail
        """
        if self._cipher_suite is not None:
            return

        self._encryption_repo = EncryptionRepository(db_session=db_session)
        self._initialize_encryption()

    def _initialize_encryption(self) -> None:
        """
        Initialize encryption by either loading existing key or generating new one.

        Raises:
            DatabaseTransactionError: If key operations fail
        """
        try:
            encryption_key, err = self._encryption_repo.get_encryption_key()
            if err:
                raise DatabaseTransactionError(
                    message="Failed to retrieve encryption key", detail=err
                )

            if encryption_key:
                self._encryption_key = encryption_key.key
            else:
                self._generate_new_key()

            self._cipher_suite = Fernet(self._encryption_key)
        except Exception as e:
            raise DatabaseTransactionError(
                message="Encryption initialization failed", detail=str(e)
            )

    def _generate_new_key(self) -> None:
        """
        Generate and store a new encryption key.

        Raises:
            DatabaseTransactionError: If key storage fails
        """
        try:
            new_key = EncryptionKey(key=Fernet.generate_key())
            err = self._encryption_repo.set_encryption_key(new_key)
            if err:
                raise DatabaseTransactionError(
                    message="Failed to store new encryption key", detail=err
                )

            self._encryption_key = new_key.key
        except Exception as e:
            raise DatabaseTransactionError(
                message="Failed to generate new encryption key", detail=str(e)
            )

    def encrypt_key(self, text: str) -> bytes:
        """
        Encrypt text using the cipher suite.

        Args:
            text (str): Text to encrypt.

        Returns:
            bytes: Encrypted data.

        Raises:
            ValueError: If encryption is not initialized.
        """
        try:
            return self._cipher_suite.encrypt(text.encode())
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}")

    def decrypt_key(self, encrypted_data: bytes) -> str:
        """
        Decrypt text using the cipher suite.

        Args:
            encrypted_data (bytes): Data to decrypt.

        Returns:
            str: Decrypted text.

        Raises:
            ValueError: If decryption is not initialized or fails.
        """
        try:
            return self._cipher_suite.decrypt(encrypted_data).decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
