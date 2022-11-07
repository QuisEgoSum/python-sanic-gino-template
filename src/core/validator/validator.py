import typing
from functools import wraps

from pydantic import ValidationError
from sanic.request import Request

from src.core.validator.enums import TargetNameEnum
from src.core.validator.exception import SchemaValidationException
from src.lib import openapi
from src.core.validator.schema import Schema
from src.common.schemas import ValidationErrorSchema
from src.utils.openapi import resolve_openapi_spec

validation_error_schema = resolve_openapi_spec(ValidationErrorSchema.schema_json())


def format_error_message(message: str, field: str) -> str:
    return message.format(field_name=field)


class Validator:
    schema: typing.Type[Schema]
    target_name: TargetNameEnum

    def __init__(
            self,
            schema: typing.Type[Schema],
            target_name: TargetNameEnum
    ):
        self.schema = schema
        self.target_name = target_name
        self.schema_fields = list(self.schema.__fields__.keys()) if target_name == TargetNameEnum.PARAMS else []

    def get_target(self, request: Request, kwargs):
        if self.target_name == TargetNameEnum.BODY:
            return request.json or dict()
        elif self.target_name == TargetNameEnum.QUERY:
            return {k: v[0] if len(v) == 1 else v for k, v in request.args.items()}
        elif self.target_name == TargetNameEnum.PARAMS:
            params = dict()
            for name in self.schema_fields:
                params[name] = kwargs[name]
            return params

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[0] if isinstance(args[0], Request) else args[1]
            target = self.get_target(request, kwargs)
            try:
                validated = self.schema.parse_obj(target)
            except ValidationError as ex:
                raise self.errors_mapper(ex)
            kwargs[self.target_name.value] = validated
            return await func(*args, **kwargs)

        openapi.response(validation_error_schema, 400)(func)
        getattr(openapi, self.target_name.value)(resolve_openapi_spec(self.schema.schema_json()))(func)
        return wrapper

    def errors_mapper(self, ex: ValidationError) -> SchemaValidationException:
        errors_list = []
        for error in ex.errors():
            loc = error['loc']
            errors_list.append(
                SchemaValidationException.SchemaValidationItemException(
                    format_error_message(error['msg'], loc[len(loc) - 1]),
                    location=loc
                )
            )
        return SchemaValidationException(
            self.target_name,
            errors_list
        )
