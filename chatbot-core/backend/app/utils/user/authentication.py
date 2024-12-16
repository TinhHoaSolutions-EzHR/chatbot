from typing import Optional

from app.models.user import User


async def get_current_user() -> Optional[User]:
    """
    Get the current user from the request
    """
    # TODO: Implement user authentication
    return User(id="f6f7b43c-c0ca-4003-8143-7c5e767cde12")
