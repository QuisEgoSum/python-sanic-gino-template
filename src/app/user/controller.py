from sanic import json

from src.app.user.schemas import CreateUser
from src.core import validator
from src.lib import openapi
from src.app.user import service


@openapi.tag('User')
@validator.body(CreateUser)
@openapi.response(CreateUser)
async def create(request, body: CreateUser):
    """Create user"""
    return json(await service.create(body))
