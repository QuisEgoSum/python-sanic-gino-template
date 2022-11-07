import os
from src.lib.openapi.utils import openapi


html_path = os.path.join(os.path.dirname(__file__), 'templates/redoc.html')

raw_html = open(html_path, 'r').read().replace('{DOC_PATH}', '/openapi')


openapi['hideUntagged'] = True
openapi['x-tagGroups'] = [
    dict(name='User', tags=['User'])
]


def get_docs():
    return raw_html

