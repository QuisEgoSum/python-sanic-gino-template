from src.app.user.enums import UserRoleEnum
from src.core.validator import Schema
from pydantic import Field, constr


class CreateUser(Schema):
    name: str = Field(min_length=1, max_length=64)
    username: str = constr(min_length=1, max_length=32, to_lower=True)
    email: str = constr(min_length=3, max_length=256, to_lower=True)
    role: UserRoleEnum
    password: str = constr(min_length=6, max_length=128)
