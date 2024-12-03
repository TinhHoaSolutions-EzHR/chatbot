from contextlib import contextmanager

from sqlalchemy.orm import Session

from app.utils.error_handler import DatabaseTransactionError


class BaseService:
    def __init__(self, db_session: Session):
        if not isinstance(db_session, Session):
            raise TypeError(f"db_session must be an instance of Session, got {type(db_session)}")

        self._db_session = db_session

    @contextmanager
    def _transaction(self):
        """
        Context manager for handling transaction
        """
        try:
            # Begin the transaction
            self._db_session.begin()

            # Yield the control back to the caller
            yield

            # Commit the transaction
            self._db_session.commit()
        except Exception as e:
            # Rollback the transaction if an exception occurs
            self._db_session.rollback()
            raise DatabaseTransactionError(message="Database transaction error", detail=str(e))
