from pydantic.main import ModelMetaclass

from src.core.validator.schema import Schema
from src.lib.openapi.spec import OpenapiRouteContent, OpenapiRouteParameterEnum
from src.lib.openapi.utils import upsert, override_handlers, object_schema_to_parameters, path as openapi_path
from src.lib.openapi.enum import STATUS_TO_DESCRIPTION
from src.utils.openapi import resolve_openapi_spec


def _resolve_schema(schema: Schema or dict) -> dict:
    return resolve_openapi_spec(schema.schema_json()) if type(schema) == ModelMetaclass else schema


def body(schema: Schema or dict, content_type='application/json'):
    spec_schema = _resolve_schema(schema)

    def inner(func):
        upsert(func).add_body_schema(content_type, spec_schema)
        return func

    return inner


def query(schema: Schema or dict):
    spec_schema = _resolve_schema(schema)

    def inner(func):
        upsert(func).add_parameters(object_schema_to_parameters(spec_schema))
        return func

    return inner


def response(schema: Schema or dict, status=200, content_type='application/json'):
    spec_schema = _resolve_schema(schema)

    def inner(func):
        upsert(func).add_response_schema(
            status,
            spec_schema,
            content_type,
            STATUS_TO_DESCRIPTION.get(status, None)
        )
        return func

    return inner


def path(schema: Schema or dict or str, path_type: str = None, description: str = '', enum=None):
    if type(schema) == ModelMetaclass:
        parameters = object_schema_to_parameters(resolve_openapi_spec(schema.schema_json()), OpenapiRouteParameterEnum.path)
    elif type(schema) == dict:
        parameters = object_schema_to_parameters(schema, OpenapiRouteParameterEnum.path)
    elif type(schema) == str:
        parameters = [openapi_path(schema, path_type, description, enum)]
    else:
        parameters = []

    def inner(func):
        upsert(func).add_parameters(parameters)
        return func

    return inner


def response_file(content_type='*/*', status=200, description=None):
    if description is None:
        description = STATUS_TO_DESCRIPTION.get(status, None)

    def inner(func):
        upsert(func).add_response_schema(
            status,
            {
                'description': 'File',
                'type': 'string',
                'format': 'binary'
            },
            content_type,
            description
        )
        return func

    return inner


def body_form_data_file(name='file', description: str = None, required=True):
    schema = {
        'type': 'object',
        'properties': {
            name: {
                'description': 'File',
                'type': 'string',
                'format': 'binary'
            }
        },
        'required': [name] if required else []
    }
    if description is not None:
        schema['description'] = description

    def inner(func):
        upsert(func).add_body_schema(
            'multipart/form-data',
            schema
        )
        return func

    return inner


def body_form_data_files(name='files', required=True, max_items=1):
    schema = {
        'type': 'object',
        'properties': {
            name: {
                'type': 'array',
                'items': {
                    'description': 'File',
                    'type': 'string',
                    'format': 'binary'
                }
            }
        },
        'required': [name] if required else []
    }
    if max_items is not None:
        schema['properties'][name]['maxItems'] = max_items

    def inner(func):
        upsert(func).add_body_schema(
            'multipart/form-data',
            schema
        )
        return func

    return inner


def body_binary(content_type='*/*'):
    def inner(func):
        upsert(func).add_body_schema(
            content_type,
            {
                'description': 'File',
                'type': 'string',
                'format': 'binary'
            }
        )
        return func

    return inner


def tag(tag_name: str, includes=None, excludes=None):
    def inner(func):
        upsert(func).add_tag_fabric(tag_name, includes, excludes)
        return func

    return inner


def exclude():
    def inner(func):
        upsert(func).exclude = True
        return func

    return inner


def handler(method: str, url: str):
    def inner(func):
        override_handlers[method + url] = func
        return func

    return inner


def no_content(status=204):
    def inner(func):
        upsert(func).add_response_content(
            status,
            OpenapiRouteContent(description='No content')
        )
        return func

    return inner


def deprecated():
    def inner(func):
        upsert(func).deprecated = True
        return func

    return inner
