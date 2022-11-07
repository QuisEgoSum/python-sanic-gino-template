import typing

from .enums import TargetNameEnum
from .validator import Validator
from .schema import Schema


def body(schema: typing.Type[Schema]):
    return Validator(schema, TargetNameEnum.BODY)


def query(schema: typing.Type[Schema]):
    return Validator(schema, TargetNameEnum.QUERY)


def params(schema: typing.Type[Schema]):
    return Validator(schema, TargetNameEnum.PARAMS)

