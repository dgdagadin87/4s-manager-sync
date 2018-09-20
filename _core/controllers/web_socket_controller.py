from aiohttp import web, WSMsgType
from ..config import settings

from ..include.helpers import json2object


class WebSocketController(web.View):

    async def get(self):

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        #request_params = self.request.rel_url.raw_parts
        #ws_name = request_params[1]

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
                    print(content_data)

            # Если отправка с ошибкой
            elif message.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())

        for ws_item in application['websockets']:
            await ws_item.send_str('main ws disconected')

        application['websockets'].remove(ws)

        print('web-socket connection closed')

        return ws
