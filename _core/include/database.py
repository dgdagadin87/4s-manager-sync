import aiomysql
from _core.config import settings


async def create_connection():
    connection = await aiomysql.connect(
        host=settings.DATABASE_HOST,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        db=settings.DATABASE_NAME
    )

    return connection


async def get_sync_links(db_cursor, link_ids=None):

    result = []

    try:
        where_section = 'linkIsOn = \'y\'' if link_ids is None else 'linkId in (' + link_ids + ')'
        sql = "SELECT * FROM sync_links sl WHERE " + where_section + " ORDER BY sl.linkName ASC"
        print(sql)
        await db_cursor.execute(sql)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def synchronize_link(name, send_method):

    from asyncio import sleep

    await send_method(settings.WS_START_SYNC, name)

    await sleep(2)

    await send_method(settings.WS_PAGE_SYNCHED, '1')

    await sleep(2)

    await send_method(settings.WS_PAGE_SYNCHED, '2')

    await sleep(2)

    await send_method(settings.WS_PAGE_SYNCHED, '3')

    await send_method(settings.WS_END_SYNC, name)
