import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2


from _core.config import settings
from _core.controllers.main_controller import MainController


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

application = web.Application()

aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader('_core/views'))

application.router.add_route('GET', '/', MainController)

application['static_root_url'] = '/static'
application.router.add_static('/static', 'static', name='static')


application.on_cleanup.append(on_shutdown)
application['websockets'] = []

'''def main():
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
        event_loop.close()'''


'''if __name__ == '__main__':
    main()'''

print('start server')
web.run_app(application, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
print('Stop server end')
