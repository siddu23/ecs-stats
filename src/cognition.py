from exceptions import *
from dbutil import *
from model import *

def health():
    result = {"state": "healthy"}
    return result

def ping_db(kwargs):
    """ping db"""
    try:
        conn = connectdb()
        cursor = conn.cursor()
        sql = """SELECT CURRENT_TIMESTAMP() as dt"""
        cursor.execute(sql)
        record_set = cursor.fetchone()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    obj = PingDB()
    for name in record_set:
        setattr(obj, name, record_set[name])
    return obj

def get_libray_added(user_id, pratilipi_ids):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT reference_id as id, state
                 FROM library.library a, library.resource b
                 WHERE a.id = b.library_id
                 AND a.state = 'ACTIVE'
                 AND b.reference_type = 'PRATILIPI'
                 AND b.state = 'ADDED'
                 AND a.user_id = {}
                 AND b.reference_id IN ({})""".format(user_id, pratilipi_ids)
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    obj_list = [ Library() for i in range(len(record_set)) ]
    for indx, row in enumerate(record_set):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list

def get_ratings(pratilipi_ids):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT reference_id as id, AVG(rating) as avg_rating
                 FROM social.review
                 WHERE reference_type = 'PRATILIPI'
                 AND state = 'PUBLISHED'
                 AND reference_id IN ({})
                 GROUP BY 1""".format(pratilipi_ids)
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    obj_list = [ Rating() for i in range(len(record_set)) ]
    for indx, row in enumerate(record_set):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list

def get_authors(author_ids):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT d.id, d.first_name, d.first_name_en, d.last_name, d.last_name_en, d.pen_name, d.pen_name_en,
                 d.firstname_lastname, d.firstnameen_lastnameen, d.slug
                 FROM author.author d
                 WHERE d.id IN ({})""".format(author_ids)
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    obj_list = [ Author() for i in range(len(record_set)) ]
    for indx, row in enumerate(record_set):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list

def get_recent_published(kwargs):
    """get recent published"""
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT COUNT(*) as cnt
                 FROM pratilipi.pratilipi a, pratilipi.categories b, pratilipi.pratilipis_categories c
                 WHERE a.id = c.pratilipi_id 
                 AND b.id = c.category_id
                 AND a.state = 'PUBLISHED'
                 AND a.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND a.language = '{}'
                 AND b.name_en = '{}'
                 AND b.type = 'SYSTEM'""".format(kwargs['language'], kwargs['category'])
        print sql
        cursor.execute(sql)
        record_count = cursor.fetchone()
        total_pratilipis = record_count.get('cnt', 0)

        sql = """SELECT a.id, a.author_id, a.content_type, a.cover_image, a.language, a.type, a.read_count_offset + a.read_count as read_count, 
                 a.title, a.title_en, a.slug, a.slug_en, a.slug_id, a.reading_time, a.updated_at
                 FROM pratilipi.pratilipi a, pratilipi.categories b, pratilipi.pratilipis_categories c
                 WHERE a.id = c.pratilipi_id 
                 AND b.id = c.category_id
                 AND a.state = 'PUBLISHED'
                 AND a.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND a.language = '{}'
                 AND b.name_en = '{}'
                 AND b.type = 'SYSTEM'
                 ORDER BY a.updated_at desc
                 LIMIT {}
                 OFFSET {}""".format(kwargs['language'], kwargs['category'], kwargs['limit'], kwargs['offset'])
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    if record_set is None: raise PratilipiNotFound

    obj_list = [ Pratilipi() for i in range(len(record_set)) ]
    for indx, row in enumerate(record_set):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list, total_pratilipis

def get_read_time(kwargs):
    """get read time based"""
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT COUNT(*) as cnt
                 FROM pratilipi.pratilipi a, pratilipi.categories b, pratilipi.pratilipis_categories c
                 WHERE a.id = c.pratilipi_id 
                 AND b.id = c.category_id
                 AND a.state = 'PUBLISHED'
                 AND a.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND a.language = '{}'
                 AND b.name_en = '{}'
                 AND b.type = 'SYSTEM'
                 AND a.reading_time BETWEEN {} AND {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'])
        print sql
        cursor.execute(sql)
        record_count = cursor.fetchone()
        total_pratilipis = record_count.get('cnt', 0)

        sql = """SELECT a.id, a.author_id, a.content_type, a.cover_image, a.language, a.type, a.read_count_offset + a.read_count as read_count, 
                 a.title, a.title_en, a.slug, a.slug_en, a.slug_id, a.reading_time, a.updated_at,
                 d.first_name, d.first_name_en, d.last_name, d.last_name_en, d.pen_name, d.pen_name_en,
                 d.firstname_lastname, d.firstnameen_lastnameen, d.slug as author_slug
                 FROM pratilipi.pratilipi a, pratilipi.categories b, pratilipi.pratilipis_categories c, author.author d
                 WHERE a.id = c.pratilipi_id 
                 AND b.id = c.category_id
                 AND a.author_id = d.id
                 AND a.state = 'PUBLISHED'
                 AND a.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND a.language = '{}'
                 AND b.name_en = '{}'
                 AND b.type = 'SYSTEM'
                 AND a.reading_time BETWEEN {} AND {}
                 ORDER BY a.reading_time desc
                 LIMIT {}
                 OFFSET {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'], kwargs['limit'], kwargs['offset'])
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    if record_set is None: raise PratilipiNotFound

    obj_list = [ Pratilipi() for i in range(len(record_set)) ]
    for indx, row in enumerate(record_set):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list, total_pratilipis

def get_high_rated(kwargs):
    """get high rated pratilipi"""
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT COUNT(*)
                 FROM (SELECT reference_id, avg(rating) as avg_rating, COUNT(*) as no_of_rating
                       FROM social.review d
                       WHERE d.reference_type = 'PRATILIPI'
                       AND d.state = 'PUBLISHED'
                       AND d.reference_id IN (SELECT a.id
                                              FROM pratilipi.pratilipi a, pratilipi.categories b, pratilipi.pratilipis_categories c
                                              WHERE a.id = c.pratilipi_id 
                                              AND b.id = c.category_id
                                              AND a.state = 'PUBLISHED'
                                              AND a.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                                              AND a.language = '{}'
                                              AND b.name_en = '{}'
                                              AND b.type = 'SYSTEM')
                       GROUP BY 1
                       HAVING avg_rating > 3.9
                       AND no_of_rating > 19) AS x""".format(kwargs['language'], kwargs['category'])
        print sql
        cursor.execute(sql)
        record_count = cursor.fetchone()
        total_pratilipis = record_count.get('cnt', 0)

        sql = """SELECT reference_id as pratilipi_id, avg(rating) as avg_rating, COUNT(*) as no_of_rating
                 FROM social.review d
                 WHERE d.reference_type = 'PRATILIPI'
                 AND d.state = 'PUBLISHED'
                 AND d.reference_id IN (SELECT a.id
                                               FROM pratilipi.pratilipi a, pratilipi.categories b, pratilipi.pratilipis_categories c
                                               WHERE a.id = c.pratilipi_id 
                                               AND b.id = c.category_id
                                               AND a.state = 'PUBLISHED'
                                               AND a.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                                               AND a.language = '{}'
                                               AND b.name_en = '{}'
                                               AND b.type = 'SYSTEM')
                 GROUP BY 1
                 HAVING avg_rating > 3.9
                 AND no_of_rating > 19
                 ORDER BY avg_rating desc, no_of_rating desc
                 LIMIT {}
                 OFFSET {}""".format(kwargs['language'], kwargs['category'], kwargs['limit'], kwargs['offset'])
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()

        rating_dict = {}
        for i in record_set:
            rating_dict[i['pratilipi_id']] = {'avg_rating': i['avg_rating']}
        pratilipi_ids = ','.join(rating_dict.keys())

        sql = """SELECT a.id, a.author_id, a.content_type, a.cover_image, a.language, a.type, a.read_count_offset + a.read_count as read_count, 
                 a.title, a.title_en, a.slug, a.slug_en, a.slug_id, a.reading_time, a.updated_at
                 FROM pratilipi.pratilipi a
                 WHERE a.id IN ({})""".format(pratilipi_ids)
        print sql
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    if record_set is None: raise PratilipiNotFound

    obj_list = [ Pratilipi() for i in range(len(record_set)) ]
    for indx, row in enumerate(record_set):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list, total_pratilipis, rating_dict

