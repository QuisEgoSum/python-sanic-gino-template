import json

from sanic import Blueprint, response as sanic_response

from src.lib.openapi import utils
from src.lib.openapi.decorators import exclude


openapi_router = Blueprint('openapi')


@openapi_router.listener('after_server_start')
def collect(app, loop):
    utils.collect(app)


@exclude()
def get_spec(request):
    return sanic_response.json(utils.openapi)


openapi_router.add_route(get_spec, '/openapi', ['GET'])


