from aiohttp import web

import aiohttp_jinja2
from ..config.settings import VIEWS_DIR


class MainController(web.View):
    @aiohttp_jinja2.template('main.html')
    async def get(self):
        return {}
