from sanic import Blueprint

from src.app.docs.router import docs_router
from src.app.user import user_router


first_version_router = Blueprint('Version')\
    .group(
        user_router,
        version=1
    )


routers = Blueprint('Common')\
    .group(
        first_version_router,
        docs_router
    )
