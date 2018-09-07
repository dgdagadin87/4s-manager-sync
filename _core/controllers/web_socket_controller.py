from aiohttp import web, WSMsgType
from ..config import settings

from ..include.helpers import json2object
from ..include.synchronize import ServerSync


class WebSocketController(web.View):

    async def _send_websocket_message(self, type, content):

        await self._ws.send_str('{"type": "%s", "content": "%s"}' % (type, content))

    async def get(self):

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        self._ws = ws

        application = self.request.app
        application['websockets'].append(ws)

        async for message in ws:

            message_type = message.type
            message_data = message.data

            message_object = json2object(message_data)
            content_type = message_object[0]
            content_data = message_object[1]

            # Если отправка без ошибки
            if message_type == WSMsgType.TEXT:

                # Команда - закрыть
                if content_type == settings.WS_CLOSE:
                    await ws.close()
                # Команда - обычный текст
                elif content_type == settings.WS_COMMON_START_SYNC:
                    server_sync = ServerSync(self._send_websocket_message, content_data)
                    await server_sync.run()

            # Если отправка с ошибкой
            elif message.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())

        application['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            _ws.send_str('main ws disconected')
        print('websocket connection closed')

        return ws
