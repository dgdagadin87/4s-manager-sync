async def get_sync_links(application):

    connection_context = application['db']

    result = []

    async with connection_context as connection, connection.cursor() as cursor:
        try:
            await cursor.execute("SELECT * FROM sync_links sl WHERE linkIsOn = 'y' ORDER BY sl.linkName ASC")
            result = await cursor.fetchall()
        except Exception as e:
            print(e)

    connection.close()

    return result
