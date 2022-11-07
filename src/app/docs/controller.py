from sanic import response
from sanic.request import Request

from src.app.docs import service
from src.lib import openapi


@openapi.exclude()
def get_docs(request: Request):
    return response.html(service.get_docs(), 200)
