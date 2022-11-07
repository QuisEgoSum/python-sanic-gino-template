import copy
import jsonref


def resolve_openapi_spec(schema):
    resolve_schema = jsonref.loads(schema, jsonschema=True)
    return copy.deepcopy(resolve_schema)
