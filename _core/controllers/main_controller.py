from aiohttp import web
import aiohttp_jinja2
import aiomysql

from .web_socket_controller import MESSAGES_LIST
from ..config import settings


class MainController(web.View):
    @aiohttp_jinja2.template('main.html')
    async def get(self):

        application = self.request.app
        connection_context = application['db']

        async with connection_context as connection, connection.cursor() as cursor:
            try:
                await cursor.execute("SELECT * FROM sync_links sl WHERE linkIsOn = 'y' ORDER BY sl.linkName ASC")
                r = await cursor.fetchall()
                print(r)
            except Exception as e:
                print(e)

        connection.close()

        return {'messages': MESSAGES_LIST}
