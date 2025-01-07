from typing import Annotated
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.settings.constants import Constants
from app.utils.user.jwt import verify_access_token

# OAuth2PasswordBearer is used to extract the token from the Authorization header.
# The `tokenUrl` parameter is only used by FastAPI's Swagger UI for testing purposes.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
) -> User:
    """
    Retrieves the current authenticated user based on the provided access token.

    Args:
        token (str): The access token extracted from the Authorization header.
        db_session (Session): The SQLAlchemy database session.

    Returns:
       User: The authenticated User object, or raises an HTTPException if invalid.
    """
    user_email = verify_access_token(token=token)

    if not user_email:
        # Raise 401 Unauthorized if the token is invalid or expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Constants.UNAUTHORIZED_REQUEST_MESSAGE,
        )

    user, error = UserService(db_session=db_session).get_user_by_email(user_email=user_email)

    if error:
        status_code, detail = error.kind
        raise HTTPException(status_code=status_code, detail=detail)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Constants.USER_NOT_FOUND_MESSAGE,
        )

    return user


def get_current_user(db_session: Session = Depends(get_db_session)) -> Optional[User]:
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
