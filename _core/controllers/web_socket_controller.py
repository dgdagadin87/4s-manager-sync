from aiohttp import web, WSMsgType

MESSAGES_LIST = []


class WebSocketController(web.View):

    async def _add_to_messages(self, message):
        MESSAGES_LIST.append({
            'message': message
        })

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        application = self.request.app
        ws.send_str('Socket was created')
        application['websockets'].append(ws)

        async for message in ws:
            if message.type == WSMsgType.TEXT:
                if message.data == 'close':
                    await ws.close()
                else:
                    result = await self._add_to_messages(message=message.data)
                    await ws.send_str('{"message": "%s"}' % (message.data))
            elif message.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())

        application['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            _ws.send_str('main ws disconected')
        print('websocket connection closed')

        return ws
