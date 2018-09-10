import aiomysql
from _core.config import settings, sql


async def create_connection():
    connection = await aiomysql.connect(
        host=settings.DATABASE_HOST,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        db=settings.DATABASE_NAME
    )

    return connection


def esacpe_string(connection, string):

    return connection.escape_string(string)


async def get_sync_links(db_cursor, link_ids=None):

    result = []

    try:
        sql_string = sql.get_sync_links(link_ids)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def get_stor_info(db_cursor, stor):

    stor_id = int(stor.get('id'))

    result = False

    try:
        sql_string = sql.get_stor_info(stor_id)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def update_stor_rate(db_cursor, stor_rate, stor_id):

    result = False

    try:
        sql_string = sql.update_stor_rate(stor_rate, stor_id)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def get_author_info(db_cursor, author_name):

    result = False

    try:
        sql_string = sql.get_author_info(author_name)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def insert_author(db_cursor, author_name, author_href):

    result = False

    try:
        sql_string = sql.insert_author(author_name, author_href)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result

