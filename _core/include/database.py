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


def escape_string(connection, string):

    return connection.escape_string(string)


async def start_sync(db_cursor, state):

    result = False

    if state:
        try:
            sql_string = sql.check_sync()
            await db_cursor.execute(sql_string)
            result = await db_cursor.fetchall()
        except Exception as e:
            print(e)

        if len(result) < 0:
            return False
        else:
            row = result[0]
            setting_value = row[2]

        if setting_value == 'true':
            return True

    try:
        sql_string = sql.start_sync(state)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


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


async def get_category_info(db_cursor, cat_name):

    result = False

    try:
        sql_string = sql.get_category_info(cat_name)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def insert_category(db_cursor, category_name, category_href):

    result = False

    try:
        sql_string = sql.insert_category(category_name, category_href)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def insert_stor(db_cursor, stor_id, stor_name, stor_href, stor_rate, stor_date, stor_desc, stor_comments, stor_watches, stor_author_id):

    result = False

    try:
        sql_string = sql.insert_stor(stor_id, stor_name, stor_href, stor_rate, stor_date, stor_desc, stor_comments, stor_watches, stor_author_id)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result

async def get_categories(db_cursor, cat_names):

    result = False

    try:
        sql_string = sql.get_categories(cat_names)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result


async def insert_cat_2_stors(db_cursor, cat_2_stors_list):

    result = False

    try:
        sql_string = sql.insert_cat_2_stors(cat_2_stors_list)
        await db_cursor.execute(sql_string)
        result = await db_cursor.fetchall()
    except Exception as e:
        print(e)

    return result
