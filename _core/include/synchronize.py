import re
import aiohttp
from lxml import html, etree
from datetime import datetime, timedelta

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
        ids      = []
        names    = []
        links    = []
        rates    = []
        descs    = []
        authors  = []
        cats     = []
        dates    = []
        watches  = []
        comments = []

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

            # Num comments
            comments_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/footer/span/span[3]/a/span")
            comments_num = '0' if len(comments_list) < 1 else ServerSync._get_stor_num_comments(comments_list[0])
            comments.insert(_cnt, comments_num)

            # Author
            author_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/footer/span[@class='white']/span[@class='autor']/a")
            author = dict() if len(author_list) < 1 else ServerSync._get_stor_author(author_list[0])
            authors.insert(_cnt, author)

            # Short desc
            desc_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/div[@class='desc']/p")
            desc = '' if len(desc_list) < 1 else ServerSync._get_stor_description(desc_list[0])
            descs.insert(_cnt, desc)

            # Date
            date_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/footer/span[@class='white']")
            date = '' if len(date_list) < 1 else ServerSync._get_stor_date(date_list[0])
            dates.insert(_cnt, date)

            # Cats
            cat_list = tree.xpath(".//*[@id='dle-content']/section[" + str(xpath_cnt) + "]/header/div[@class='parent']")
            cur_cats = dict if len(cat_list) < 1 else ServerSync._get_stor_cats(cat_list[0])
            cats.insert(_cnt, cur_cats)

        page_collection = ServerSync._get_page_collection(ids, names, links, rates, descs, authors, cats, dates, watches, comments)
        print(page_collection)

    @staticmethod
    def _get_stor_id(element):

        story_link = str(element.get('href'))
        link_array = story_link.split('/')
        id_and_name = link_array[-1]
        id_and_name_array = id_and_name.split('-')

        return id_and_name_array[0]

    @staticmethod
    def _get_stor_name(element):

        return element.text_content()

    @staticmethod
    def _get_stor_link(element):

        return element.get('href')

    @staticmethod
    def _get_stor_rate(element):

        return element.text_content()

    @staticmethod
    def _get_stor_num_watches(element):

        value = element.text_content()
        value_list = re.split(r'\s*:\s*', value)
        watches = value_list[1]
        watches = watches.replace(' ', '')
        watches = int(watches)
        return watches

    @staticmethod
    def _get_stor_num_comments(element):

        value = str(element.text_content())
        value = '0' if value == '' else int(value)
        return value

    @staticmethod
    def _get_stor_author (element):

        return_array = dict()
        user_name = element.text_content()
        return_array['name'] = user_name
        return_array['href'] = '//4stor.ru/' + user_name
        return return_array

    @staticmethod
    def _get_stor_description(element):

        short_desc = etree.tostring(element, encoding='utf8', method='xml')
        return short_desc.decode('utf8')

    @staticmethod
    def _get_stor_date(element):

        text_content = element.text_content()

        match = re.search(r'(.*?),\s*(\d\d:\d\d)', text_content)
        if match:
            match_list = re.split(r'\s*,\s*', match[0])
            stor_date = match_list[0]
            stor_time = match_list[1] + ':00'
            return ServerSync._prepare_date(stor_date, stor_time)
        else:
            return ''

    @staticmethod
    def _prepare_date(raw_date, raw_time):

        now_time = datetime.now()

        raw_time_list = raw_time.split(':')

        if re.search(r'вчера', raw_date, re.I):
            yesterday_time = datetime(2018, 9, 1) - timedelta(days=1)
            return str(datetime(
                yesterday_time.year,
                yesterday_time.month,
                yesterday_time.day,
                int(raw_time_list[0]),
                int(raw_time_list[1]),
                0
            ))
        elif re.search(r'сегодня', raw_date, re.I):
            return str(datetime(
                now_time.year,
                now_time.month,
                now_time.day,
                int(raw_time_list[0]),
                int(raw_time_list[1]),
                0
            ))

        date = raw_date.split('-')
        return str(datetime(int(date[2]), int(date[1]), int(date[0]), int(raw_time_list[0]), int(raw_time_list[1]), 0))

    @staticmethod
    def _get_stor_cats(element):

        text_content = element.text_content()

        stor_cats = re.split(r'\s*\/\s*', text_content)

        if len(stor_cats) < 1:
            return []

        return stor_cats

    @staticmethod
    def _get_page_collection(stor_ids, stor_names, stor_links, stor_rates, stor_descs, stor_authors, stor_cats, stor_dates, stor_watches, stor_comments):

        result = []

        for i in range(len(stor_ids)):

            current_stor = {
                'name'    : stor_names[i],
                'link'    : stor_links[i],
                'rate'    : stor_rates[i],
                'watches' : stor_watches[i],
                'comments': stor_comments[i],
                'date'    : stor_dates[i],
                'desc'    : stor_descs[i],
                'author'  : stor_authors[i],
                'cats'    : stor_cats[i]
            }

            result.insert(i, current_stor)

        return result
