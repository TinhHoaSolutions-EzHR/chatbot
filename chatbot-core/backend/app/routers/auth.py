from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.services.user import UserService
from app.services.user import UserSettingService
from app.settings.constants import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger
from app.utils.user.jwt import create_access_token

# Initialize logger
logger = get_logger(__name__)

# Define the router for authentication-related endpoints
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/oauth/google", status_code=status.HTTP_200_OK, response_model=APIResponse)
def get_oauth_access_token(code: str, db_session: Session = Depends(get_db_session)):
    """
    Retrieves OAuth access token and stores user information in the database if not already present.

    Args:
        code (str): The authorization code from Google OAuth.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        APIResponse: The response containing the access token and token type.
    """
    user_oauth_data, err = UserService(db_session=db_session).get_user_from_google_oauth(code=code)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    user, err = UserService(db_session=db_session).get_user_by_email(
        email=user_oauth_data.get("email")
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    if not user:
        # Create a new user if not already present
        user, err = UserService(db_session=db_session).create_user(user_oauth_data=user_oauth_data)
        if err:
            status_code, detail = err.kind
            raise HTTPException(status_code=status_code, detail=detail)

        logger.info("Created user successfully.")

        # Create a new user setting
        err = UserSettingService(db_session=db_session).create_user_settings(user_id=user.id)
        if err:
            status_code, detail = err.kind
            raise HTTPException(status_code=status_code, detail=detail)

        logger.info("Created user settings successfully.")

    elif not user.is_oauth:
        # If the user already exists with a different login method, return an error
        status_code, detail = ErrorCodesMappingNumber.USER_WRONG_LOGIN_METHOD.value
        raise HTTPException(
            status_code=status_code,
            detail=detail,
        )

    access_token = create_access_token(data=user_oauth_data.get("email"))

    return (
        BackendAPIResponse()
        .set_message(Constants.API_SUCCESS)
        .set_data({"access_token": access_token, "token_type": "bearer"})
        .respond()
    )
