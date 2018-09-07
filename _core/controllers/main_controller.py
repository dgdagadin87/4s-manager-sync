from aiohttp import web
import aiohttp_jinja2

from ..include.database import create_connection, get_sync_links


class MainController(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):

        db_context = await create_connection()

        async with db_context as connection, connection.cursor() as cursor:
            sync_links = await get_sync_links(cursor)

        connection.close()

        return {'sync_links': sync_links}
