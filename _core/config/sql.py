def get_sync_links(link_ids):

    where_section = 'linkIsOn = \'y\'' if link_ids is None else 'linkId in (' + link_ids + ')'
    return 'SELECT * FROM sync_links sl WHERE ' + where_section + ' ORDER BY sl.linkName ASC'


def get_stor_info(stor_id):

    return 'SELECT storId FROM stories WHERE storId = \'' + str(stor_id) + '\''


def update_stor_rate(rate, id):

    return 'UPDATE `stories` SET `storRate` = \'' + rate + '\' WHERE `storId` = \'' + str(id) + '\''


def get_author_info(name):

    return 'SELECT `authorId` FROM `authors` WHERE `authorName` = \'' + name + '\''


def insert_author(name, href):

    return 'INSERT INTO `authors` (authorName, authorHref) VALUES (\'' + name + '\', \'' + href + '\')'
