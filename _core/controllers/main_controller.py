from aiohttp import web
import aiohttp_jinja2

from .web_socket_controller import MESSAGES_LIST


class MainController(web.View):
    @aiohttp_jinja2.template('main.html')
    async def get(self):
        return {'messages': MESSAGES_LIST}
