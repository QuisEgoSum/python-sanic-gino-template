import typing

from src.core.config.project import project_metadata
from src.lib.openapi.spec import OpenapiRoute, OpenapiRouteParameter, OpenapiRouteParameterEnum, OpenapiRouteContent

openapi = dict(
    paths={},
    info={'title': project_metadata['name'], 'version': project_metadata['version']},
    openapi="3.0.3",
    tags=[],
    servers=[
        {'url': 'http://localhost:8080'}
    ]
)
handlers = dict()
override_handlers = dict()


def get_openapi_from_handler(route_handler) -> OpenapiRoute:
    spec: OpenapiRoute = OpenapiRoute()
    while True:
        if route_handler in handlers:
            spec.merge(handlers[route_handler])
        if hasattr(route_handler, '__wrapped__'):
            route_handler = route_handler.__wrapped__
        else:
            return spec


def extract_methods_url(bg, route):
    url = ''
    if bg.url_prefix:
        url = bg.url_prefix
    for part in route[1].split('/'):
        if part == '':
            continue
        if part.startswith('<'):
            url += '/{' + part.split(':')[0].replace('>', '').replace('<', '') + '}'
        else:
            url += '/' + part
    methods = [*route.methods]
    return url, methods


def extract_route_handler(route, method, url):
    route_handlers = list(filter(
        lambda h: h is not None,
        [
            override_handlers.get(method + url, None),
            route.handler
        ]
    ))
    return route_handlers[0]


def collect(app):
    tags = set()
    for bg_name in app.blueprints.keys():
        bg = app.blueprints[bg_name]
        for route in bg.routes:
            methods = list(route.methods)
            url = route.uri
            for method in methods:
                method = method.lower()
                if method == 'options':
                    continue
                handler = extract_route_handler(route, method, url)
                openapi_route = get_openapi_from_handler(handler) or OpenapiRoute()
                if openapi_route.exclude is True:
                    continue
                openapi_route.resolve_tags(url, bg_name)
                tags = tags.union(openapi_route.tags)
                openapi_route.summary = handler.__doc__ or ''
                if len(openapi_route.responses) == 0:
                    openapi_route.add_response_content(200, OpenapiRouteContent(description='Ok'))
                if url not in openapi['paths']:
                    openapi['paths'][url] = {method: openapi_route.to_dict()}
                else:
                    openapi['paths'][url][method] = openapi_route.to_dict()
    openapi['tags'] = [dict(name=name) for name in tags]


def upsert(func) -> OpenapiRoute:
    if func not in handlers:
        handlers[func] = OpenapiRoute()
    return handlers[func]


def object_schema_to_parameters(
        schema: dict,
        location: OpenapiRouteParameterEnum = OpenapiRouteParameterEnum.query
) -> typing.List[OpenapiRouteParameter]:
    parameters = []
    required = set(schema.get('required', []))

    for prop in schema['properties'].items():
        name = prop[0]
        item = prop[1]
        parameters.append(
            OpenapiRouteParameter(
                location,
                name,
                name in required,
                item
            )
        )
    return parameters


def path(name, path_type, description=None, enum=None):
    schema = {
        'type': path_type
    }
    if enum is not None:
        if type(enum) != list:
            enum = enum.list()
        schema['enum'] = enum
    return OpenapiRouteParameter(
        OpenapiRouteParameterEnum.path,
        name,
        True,
        schema,
        description
    )
