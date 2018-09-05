from aiohttp import web

from ..config.settings import VIEWS_DIR


async def main_controller(request):

    with open(VIEWS_DIR + '/main.html', 'rb') as file:
        return web.Response(
            body=file.read().decode('utf8'),
            content_type='text/html'
        )
