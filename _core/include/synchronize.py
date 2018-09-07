from ..config import settings
from .database import create_connection, get_sync_links, synchronize_link


class ServerSync(object):

    def __init__(self, send_method, link_ids):

        self._websocket_send = send_method
        self._link_ids = link_ids

    async def run(self):

        # Старт синхронизации
        await self._start_synchronize()

        # Соединение к БД
        await self._create_connection()

        # Получение списка синхронизируемых категорий
        await self._get_sync_links()

        # Синхронизация каждой категории
        for link in self._sync_links:
            await self._synchronize_link(link)

        # Закрытие соединения к БД
        self._close_connection()

        # Окончание синхронизации
        await self._end_synchronize()

    async def _start_synchronize(self):
        await self._websocket_send(type=settings.WS_COMMON_START_SYNC, content='')

    async def _end_synchronize(self):
        await self._websocket_send(type=settings.WS_COMMON_END_SYNC, content='')

    async def _create_connection(self):
        self._db_connection = await create_connection()
        self._db_cursor = await self._db_connection.cursor()

    def _close_connection(self):
        self._db_connection.close()

    async def _get_sync_links(self):
        self._sync_links = await get_sync_links(self._db_cursor, link_ids=self._link_ids)

    async def _synchronize_link(self, link):
        await synchronize_link (link[1], self._websocket_send)
