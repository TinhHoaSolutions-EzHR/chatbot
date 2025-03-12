from contextlib import contextmanager

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

from app.exception.database_exceptions import DatabaseOperationalException


class BaseRepository:
    def __init__(self, db_session: Session):
        """
        Base repository class for handling database operations.

        Args:
            db_session (Session): Database session
        """
        if not isinstance(db_session, Session):
            raise TypeError(f"db_session must be an instance of Session, got {type(db_session)}")

        self._db_session = db_session

    @contextmanager
    def _db_error_handling(self, operation: str):
        try:
            yield
        except OperationalError as e:
            pass
        except IntegrityError as e:
            pass
        except SQLAlchemyError as e:
            pass
        except Exception as e:
            raise DatabaseOperationalException(str(e))