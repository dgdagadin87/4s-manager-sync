from aiohttp import web
import aiohttp_jinja2


class MainController(web.View):
    @aiohttp_jinja2.template('main.html')
    async def get(self):
        return {}
