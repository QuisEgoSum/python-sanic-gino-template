import traceback

from sanic import Sanic, Request, response
from sanic.exceptions import SanicException
from sanic.log import logger

from src.core.exception import ApplicationException


def exception_handlers(server: Sanic):
    @server.exception(ApplicationException)
    def application_exception_handler(request: Request, exception: ApplicationException):
        payload = exception.to_dict()
        logger.error(payload)
        return response.json(payload, status=exception.status_code)

    @server.exception(SanicException)
    def sanic_exceptions(request: Request, exception: SanicException):
        payload = dict(message=str(exception))
        logger.error(payload)
        return response.json(payload, status=exception.status_code)

    @server.exception(Exception)
    def internal_server_exception_handler(request: Request, exception: Exception):
        logger.fatal(traceback.format_exc())
        return response.json(dict(message='Internal Server Error', code=4, error='InternalServerException'), status=500)
