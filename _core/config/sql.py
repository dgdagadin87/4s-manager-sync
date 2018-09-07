def get_sync_links(link_ids):

    where_section = 'linkIsOn = \'y\'' if link_ids is None else 'linkId in (' + link_ids + ')'
    return 'SELECT * FROM sync_links sl WHERE ' + where_section + ' ORDER BY sl.linkName ASC'