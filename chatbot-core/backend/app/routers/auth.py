from sqlalchemy.orm import Session
from app.databases.mssql import get_db_session
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.settings.constants import Constants
from app.settings.secrets import Secrets
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi import status
from fastapi.responses import JSONResponse
import requests

from app.utils.api.helpers import get_logger
from app.utils.api.api_response import APIResponse
from app.utils.user.authentication import format_bearer
from app.utils.user.jwt import create_access_token


logger = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/oauth/google", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_oauth_access_token(
    code: str, response: Response, db_session: Session = Depends(get_db_session)
):
    """
    Get OAuth access token, store user info in database if not exists.

    Returns:
        APIResponse: API response
    """
    data = {
        "code": code,
        "client_id": Constants.GOOGLE_CLIENT_ID,
        "client_secret": Secrets.GOOGLE_CLIENT_SECRET,
        "redirect_uri": Constants.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    google_response = requests.post(Constants.GOOGLE_TOKEN_URL, data=data)
    access_token = google_response.json().get("access_token")
    user_info = requests.get(
        Constants.GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    user, err = UserService(db_session=db_session).get_user_by_email(user_info.email)

    if err:
        status_code, detail = err.kind
        raise HTTPException(status_code=status_code, detail=detail)

    if not user:
        return None

    if not user.is_oauth:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=Constants.USER_WRONG_LOGIN_METHOD
        )

    access_token = create_access_token(user.email)

    response.set_cookie(key=Constants.EZHR_ACCESS_TOKEN, value=format_bearer(access_token))

    return None


@router.get("/logout", response_model=APIResponse, status_code=status.HTTP_200_OK)
def logout(response: Response):
    """
    Logout user.

    Returns:
        APIResponse: API response
    """
    response.delete_cookie(key=Constants.EZHR_ACCESS_TOKEN)

    return None
