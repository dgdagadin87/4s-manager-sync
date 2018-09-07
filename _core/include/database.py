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


async def get_sync_links():

    connection_context = await create_connection()

    result = []

    async with connection_context as connection, connection.cursor() as cursor:
        try:
            await cursor.execute("SELECT * FROM sync_links sl WHERE linkIsOn = 'y' ORDER BY sl.linkName ASC")
            result = await cursor.fetchall()
        except Exception as e:
            print(e)

    connection.close()

    return result
