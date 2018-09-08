import re
import aiohttp
from lxml import html

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
        await self._close_connection()

        # Окончание синхронизации
        await self._end_synchronize()

    async def _start_synchronize(self):
        await self._websocket_send(type=settings.WS_COMMON_START_SYNC, content='')

    async def _end_synchronize(self):
        await self._websocket_send(type=settings.WS_COMMON_END_SYNC, content='')

    async def _create_connection(self):
        self._db_connection = await create_connection()
        self._db_cursor = await self._db_connection.cursor()

    async def _close_connection(self):
        await self._db_cursor.close()
        self._db_connection.close()

    async def _get_sync_links(self):
        self._sync_links = await get_sync_links(self._db_cursor, link_ids=self._link_ids)

    async def _synchronize_link(self, link):

        link_name = link[1]
        is_link_multipage = True if link[4] == 'y' else False

        await self._websocket_send(settings.WS_START_SYNC, link_name)

        if is_link_multipage:
            for i in range(100000):
                page_href = link[2] + 'page/' + str(i) + '/'
                sync_page_result = await self._synchronize_page(page_href)
                if sync_page_result is None:
                    await self._websocket_send(settings.WS_END_SYNC, link_name)
                    break
        else:
            await self._synchronize_page(link[2])
            await self._websocket_send(settings.WS_END_SYNC, link_name)

    async def _synchronize_page(self, page_href):

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(page_href) as response:
                    page_response = await response.text()
        except Exception as e:
            print(e)
            return False

        # инициализация
        ids = names = links = rates = descs = authors = cats = dates = watches = comments = []

        # начало парсинга
        tree = html.fromstring(page_response)

        # Id, Name, link
        elements = tree.xpath(".//*[@class='story_item']/header/h2/a")

        if len(elements) > 0:

            counter = 0

            for element in elements:
                id = ServerSync._get_stor_id(element)
                name = ServerSync._get_stor_name(element)
                link = ServerSync._get_stor_link(element)

                ids.insert(counter, id)
                names.insert(counter, name)
                links.insert(counter, link)

                counter += 1

        if len(ids) < 1:
            return None

        for _cnt in range(len(ids)):

            xpath_cnt = _cnt + 1

            # Rating
            rating_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/header/h2/div/span")
            rate = '0' if len(rating_list) < 1 else ServerSync._get_stor_rate(rating_list[0])
            rates.insert(_cnt, rate)

            # Num watches
            watches_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/footer/span/span[2]")
            watches_num = 0 if len(watches_list) < 1 else ServerSync._get_stor_num_watches(watches_list[0])
            watches.insert(_cnt, watches_num)

    @staticmethod
    def _get_stor_id(self, element):

        story_link = str(element.get('href'))
        link_array = story_link.split('/')
        id_and_name = link_array[-1]
        id_and_name_array = id_and_name.split('-')

        return id_and_name_array

    @staticmethod
    def _get_stor_name(self, element):

        return element.text_content()

    @staticmethod
    def _get_stor_link(self, element):

        return element.get('href')

    @staticmethod
    def _get_stor_rate(self, element):

        return element.text_content()

    @staticmethod
    def _get_stor_num_watches(self, element):

        value = element.text_content()
        value_list = re.split(r'\s*:\s*', value)
        watches = value_list[1]
        watches = watches.replace(' ', '')
        watches = int(watches)
        return watches

