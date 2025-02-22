from sqlalchemy.orm import Session


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
