from fastapi import APIRouter

from app.routers import auth
from app.routers import base
from app.routers.v1 import agent
from app.routers.v1 import background
from app.routers.v1 import chat
from app.routers.v1 import connector
from app.routers.v1 import folder
from app.routers.v1 import provider
from app.routers.v1 import user
from app.settings import Constants
from app.utils.api.helpers import get_logger

# root_path = os.getenv("ROOT_PATH", "/backend")

logger = get_logger(__name__)
logger.info("Including routers")

api_router = APIRouter()

api_router.include_router(router=base.router)
api_router.include_router(router=auth.router)
api_router.include_router(router=connector.router, prefix=Constants.FASTAPI_PREFIX)
api_router.include_router(router=chat.router, prefix=Constants.FASTAPI_PREFIX)
api_router.include_router(router=folder.router, prefix=Constants.FASTAPI_PREFIX)
api_router.include_router(router=agent.router, prefix=Constants.FASTAPI_PREFIX)
api_router.include_router(router=user.router, prefix=Constants.FASTAPI_PREFIX)
api_router.include_router(router=provider.router, prefix=Constants.FASTAPI_PREFIX)
api_router.include_router(router=background.router, prefix=Constants.FASTAPI_PREFIX)
