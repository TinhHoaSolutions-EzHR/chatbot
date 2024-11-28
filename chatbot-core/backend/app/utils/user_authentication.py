from models.user import User


async def get_current_user() -> User | None:
    # TODO: Implement user authentication
    return User(id="123")
