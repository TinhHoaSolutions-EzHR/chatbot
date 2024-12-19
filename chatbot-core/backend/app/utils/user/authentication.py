from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.user import User
from app.repositories.user import UserRepository


async def get_current_user(db_session: Session = Depends(get_db_session)) -> Optional[User]:
    """
    Get the current user from the request

    Args:
        db_session (Session): Database session

    Returns:
        Optional[User]: User object
    """
    # TODO: Implement user authentication
    user_id = "f6f7b43c-c0ca-4003-8143-7c5e767cde12"
    user, err = UserRepository(db_session=db_session).get_user(user_id=user_id)

    return user if not err else None
