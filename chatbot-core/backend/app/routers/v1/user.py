from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models import User
from app.models.user import UserSettingRequest
from app.services.user import UserService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.error_handler import ErrorCodesMappingNumber
from app.utils.api.helpers import get_logger
from app.utils.user.authentication import get_current_user

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["user", "setting"])


@router.patch("/settings", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_user_settings(
    user_setting_request: UserSettingRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Update user settings.

    Args:
        user_request (UserRequest): User request object
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
    err = UserService(db_session=db_session).update_user_settings(
        user=user,
        user_setting_request=user_setting_request,
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse user settings
    data = user_setting_request.model_dump(exclude_unset=True)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()
