import asyncio
from aiohttp import web

from ..include.synchronize import ServerSync
from ..include.helpers import object2string


class StartSyncController(web.View):

    def _start_server_sync(self, ids):

        application = self.request.app

        async def async_method():

            server_sync = ServerSync(self.send_2_user, self._actualize_data, application, ids)
            await server_sync.run()

        asyncio.ensure_future(async_method())

    def _actualize_data(self, data):

        self.request.app['send_object'] = data

    async def _send_websocket_message(self, content):

        application = self.request.app

        web_sockets = application['websockets']

        for ws_item in web_sockets:
            await ws_item.send_str(content)

    async def send_2_user(self, data):

        self._actualize_data(data)
        await self._send_websocket_message(object2string(data))

    async def get(self):

        query = self.request.query
        items = query.get('items')

        self._start_server_sync(items)

        return web.Response(body=b'OK')