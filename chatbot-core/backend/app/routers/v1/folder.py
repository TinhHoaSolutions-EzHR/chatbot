from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.databases.mssql import get_db_session
from app.models import User
from app.models.folder import FolderRequest
from app.models.folder import FolderResponse
from app.services.folder import FolderService
from app.settings import Constants
from app.utils.api.api_response import APIResponse
from app.utils.api.api_response import BackendAPIResponse
from app.utils.api.helpers import get_logger
from app.utils.user.authentication import get_current_user


logger = get_logger(__name__)
router = APIRouter(prefix="/folders", tags=["folders", "chat", "session", "message"])


@router.get("", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_folders(
    db_session: Session = Depends(get_db_session), user: User = Depends(get_current_user)
) -> BackendAPIResponse:
    """
    Get all chat folders of the user.

    Args:
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    user_id = user.id if user else None

    # Get chat folders of user
    folders, err = FolderService(db_session=db_session).get_folders(user_id=user_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat folders
    if folders:
        data = [FolderResponse.model_validate(folder) for folder in folders]
    else:
        data = []

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_folder(
    folder_request: FolderRequest, db_session: Session = Depends(get_db_session), user: User = Depends(get_current_user)
) -> BackendAPIResponse:
    """
    Create a new chat folder.

    Args:
        folder_request (FolderRequest): Folder request object
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    user_id = user.id if user else None

    # Create chat folder
    err = FolderService(db_session=db_session).create_folder(folder_request=folder_request, user_id=user_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat folder
    data = folder_request.model_dump(exclude_unset=True)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.patch("/{folder_id}", response_model=APIResponse, status_code=status.HTTP_200_OK)
def update_folder(
    folder_id: str,
    folder_request: FolderRequest,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Update chat folder by ID.

    Args:
        folder_id (str): Folder ID
        folder_request (FolderRequest): Folder request object
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    user_id = user.id if user else None

    # Update chat folder
    err = FolderService(db_session=db_session).update_folder(
        folder_id=folder_id, folder_request=folder_request, user_id=user_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    # Parse chat folder
    data = folder_request.model_dump(exclude_unset=True)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=data).respond()


@router.delete("/{folder_id}", response_model=APIResponse, status_code=status.HTTP_204_NO_CONTENT)
def delete_folder(
    folder_id: str, db_session: Session = Depends(get_db_session), user: User = Depends(get_current_user)
) -> BackendAPIResponse:
    """
    Delete chat folder by ID.

    Args:
        folder_id (str): Folder ID
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    user_id = user.id if user else None

    # Delete chat folder
    err = FolderService(db_session=db_session).delete_folder(folder_id=folder_id, user_id=user_id)
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).respond()


@router.post(
    "/{folder_id}/chat_sessions/{chat_session_id}", response_model=APIResponse, status_code=status.HTTP_201_CREATED
)
def add_chat_session_to_folder(
    folder_id: str,
    chat_session_id: str,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> BackendAPIResponse:
    """
    Add chat session to chat folder.

    Args:
        folder_id (str): Folder ID
        chat_session_id (str): Chat session ID
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object

    Returns:
        BackendAPIResponse: API response
    """
    user_id = user.id if user else None

    # Add chat session to chat folder
    err = FolderService(db_session=db_session).add_chat_session_to_folder(
        folder_id=folder_id, chat_session_id=chat_session_id, user_id=user_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    return BackendAPIResponse().set_message(message=Constants.API_SUCCESS).set_data(data=None).respond()


@router.delete("/{folder_id}/chat_sessions/{chat_session_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_chat_session_from_folder(
    folder_id: str,
    chat_session_id: str,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> None:
    """
    Remove chat session from chat folder.

    Args:
        folder_id (str): Folder ID
        chat_session_id (str): Chat session ID
        db_session (Session): Database session. Defaults to relational database session.
        user (User): User object
    """
    user_id = user.id if user else None

    # Remove chat session from chat folder
    err = FolderService(db_session=db_session).remove_chat_session_from_folder(
        folder_id=folder_id, chat_session_id=chat_session_id, user_id=user_id
    )
    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)
