from aiohttp import web
import aiohttp_jinja2

from ..include.database import get_sync_links


class MainController(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):

        sync_links = await get_sync_links(self.request.app)
        return {'sync_links': sync_links}
