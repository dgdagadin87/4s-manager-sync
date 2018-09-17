def start_sync(state):

    insert_state = 'true' if state else 'false'
    return 'UPDATE `settings` SET settingValue = \'' + insert_state + '\' WHERE settingName = \'is_sync\''


def check_sync():

    return 'SELECT * FROM `settings` WHERE settingName = \'is_sync\''


def get_sync_links(link_ids):

    where_section = 'linkIsOn = \'y\'' if link_ids is None else 'linkId in (' + link_ids + ')'
    return 'SELECT * FROM `sync_links` sl WHERE ' + where_section + ' ORDER BY sl.linkName ASC'


def get_stor_info(stor_id):

    return 'SELECT `storId` FROM `stories` WHERE storId = \'' + str(stor_id) + '\''


def update_stor_rate(rate, id):

    return 'UPDATE `stories` SET `storRate` = \'' + rate + '\' WHERE `storId` = \'' + str(id) + '\''


def get_author_info(name):

    return 'SELECT `authorId` FROM `authors` WHERE `authorName` = \'' + name + '\''


def insert_author(name, href):

    return 'INSERT INTO `authors` (authorName, authorHref) VALUES (\'' + name + '\', \'' + href + '\')'


def get_category_info(name):

    return 'SELECT `catId` FROM `categories` WHERE `catName` = \'' + name + '\''


def get_categories(names):

    return 'SELECT `catId` FROM `categories` WHERE `catName` IN (' + ', '.join(names) + ')'


def insert_category(name, href):

    return 'INSERT INTO `categories` (catName, catHref) VALUES (\'' + name + '\', \'' + href + '\')'


def insert_stor(id, name, href, rate, date, desc, comments, watches, author_id):

    return 'INSERT INTO `stories` (storId, storName, storHref, storRate, storDate, storDesc, storAuthorId, storWatches, storComments) VALUES (\'' + id + '\', \'' + name + '\', \'' + href + '\' , \'' + rate + '\', \'' + date + '\', \'' + desc + '\', \'' + author_id + '\', \'' + watches + '\', \'' + comments + '\')'


def insert_cat_2_stors(cat_2_stors_list):

    return 'INSERT INTO `cats2stories` (catId, storId) VALUES ' + ', '.join(cat_2_stors_list)
