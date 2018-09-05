import asyncio
from aiohttp import web

from _core.config import settings
from _core.controllers.main_controller import main_controller


application = web.Application()

application.router.add_route('GET', '/', main_controller)


def main():
    event_loop = asyncio.get_event_loop()
    handler = application.make_handler()
    f = event_loop.create_server(handler, settings.SERVER_HOST, settings.SERVER_PORT)
    server = event_loop.run_until_complete(f)

    async def end():
        await handler.finish_connections(1.0)
        server.close()
        await server.wait_closed()
        await application.finish()

    print('serving on', server.sockets[0].getsockname())
    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        event_loop.run_until_complete(end())
        event_loop.close()


if __name__ == '__main__':
    main()
