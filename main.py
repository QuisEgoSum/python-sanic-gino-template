from src.core.db import connect
from src.server.http import create_http_server, run


def main():
    http_server = create_http_server()
    http_server.register_listener(start, 'after_server_start')
    http_server.register_listener(shutdown, 'before_server_stop')
    return run(http_server)


async def start(server):
    await connect()


async def shutdown(server):
    pass


if __name__ == '__main__':
    main()

