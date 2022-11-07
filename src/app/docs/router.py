from sanic import Blueprint
from src.app.docs.controller import get_docs


docs_router = Blueprint('docs')
docs_router.add_route(get_docs, '/docs', ['GET'])
