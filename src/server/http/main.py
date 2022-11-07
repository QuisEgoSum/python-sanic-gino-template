from sanic import Sanic
from sanic_cors import CORS
from src.app import routers
from src.core.config import config
from src.lib.openapi import openapi_router
from src.server.http.modules.logger import logger_config
from src.server.http.modules.exception_handler import exception_handlers


def create_http_server() -> Sanic:
    server = Sanic('HttpServer', log_config=logger_config)
    CORS(server)
    exception_handlers(server)
    server.blueprint(openapi_router)
    server.blueprint(routers)
    return server


def run(server: Sanic):
    server_config = config.server.http
    return server.run(
        host=server_config.host,
        port=server_config.port,
        workers=server_config.workers,
        debug=config.debug
    )



