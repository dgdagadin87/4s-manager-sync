from aiohttp import web
import aiohttp_jinja2

from ..include.database import create_connection, get_sync_links


class MainController(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):

        db_connection = await create_connection()

        cursor = await db_connection.cursor()

        sync_links = await get_sync_links(cursor)

        await cursor.close()

        db_connection.close()

        return {'sync_links': sync_links}
