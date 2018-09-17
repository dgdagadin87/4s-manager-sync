from aiohttp import web
import aiohttp_jinja2
import jinja2

from _core.config import settings
from _core.controllers.main_controller import MainController
from _core.controllers.web_socket_controller import WebSocketController


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

application = web.Application()

aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader('_core/views'))

application.router.add_route('GET', '/', MainController)
application.router.add_route('GET', '/{id}/ws', WebSocketController)

application['static_root_url'] = '/static'
application.router.add_static('/static', 'static', name='static')

application.on_cleanup.append(on_shutdown)
application['websockets'] = []

print('start server')
web.run_app(application, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
print('Stop server end')
