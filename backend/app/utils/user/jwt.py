from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

import jwt

from app.settings import Constants
from app.settings import Secrets


def create_access_token(data: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create access token.

    Args:
        data (string): Data for encoding

    Returns:
        str: Access token
    """
    to_encode = {"sub": data}

    if expires_delta:
        expiration = datetime.now(timezone.utc) + expires_delta
    else:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=Constants.JWT_EXPIRATION)

    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, Secrets.JWT_SECRET, algorithm=Constants.JWT_ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> Optional[str]:
    """
    Verify access token.

    Args:
        token (str): Access token

    Returns:
        Optional[str]: Decoded token
    """
    try:
        payload = jwt.decode(token, Secrets.JWT_SECRET, algorithms=[Constants.JWT_ALGORITHM])
        data: str = payload.get("sub")

        if data is None:
            return None

        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except:
        return None
