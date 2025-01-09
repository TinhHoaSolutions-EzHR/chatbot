from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models import User
from app.models.user import UserResponse
from app.models.user import UserSettingsRequest
from app.models.user import UserSettingsResponse
from app.services.user import UserSettingService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger
from app.utils.user.authentication import get_current_user_from_token

logger = get_logger(__name__)
router = APIRouter(prefix="/users/me", tags=["user", "setting"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_user(
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Get user.

    Args:
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    # Parse user
    data = UserResponse.model_validate(user)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.get("/settings", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_user_settings(
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Get user settings.

    Args:
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    # Get user settings
    user_settings, err = UserSettingService(db_session=db_session).get_user_settings(
        user_id=user.id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse user settings
    if user_settings:
        data = UserSettingsResponse.model_validate(user_settings)
    else:
        data = None

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )


@router.patch("/settings", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_user_settings(
    user_settings_request: UserSettingsRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user_from_token),
) -> BackendAPIResponse:
    """
    Update user settings.

    Args:
        user_settings_request (UserRequest): User settings request object
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    if not user:
        status_code, detail = ErrorCodesMappingNumber.UNAUTHORIZED_REQUEST.value
        raise HTTPException(
            status_code=status_code,
            detail=detail,
        )

    # Update user settings
    err = UserSettingService(db_session=db_session).update_user_settings(
        user_id=user.id,
        user_settings_request=user_settings_request,
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse user settings
    data = user_settings_request.model_dump(exclude_unset=True)

    return (
        BackendAPIResponse()
        .set_message(message=Constants.API_SUCCESS)
        .set_data(data=data)
        .respond()
    )
