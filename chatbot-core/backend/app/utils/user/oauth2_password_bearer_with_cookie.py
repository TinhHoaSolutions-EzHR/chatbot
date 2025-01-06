from typing import Dict
from typing import Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from app.settings.constants import Constants


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Custom OAuth2 security scheme that retrieves the access token
    from an HTTP-only cookie instead of the Authorization header.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        # If no scopes are provided, initialize an empty dictionary
        if not scopes:
            scopes = {}

        # Create an OAuthFlowsModel instance with the password flow
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})

        # Initialize the parent OAuth2 class with the flows, scheme name, and error handling
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(Constants.EZHR_ACCESS_TOKEN)

        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            # If auto_error is True, raise an HTTP 401 Unauthorized error
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=Constants.UNAUTHORIZED_REQUEST_MESSAGE,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        # Return the access token (the parameter part of the Bearer scheme)
        return param
