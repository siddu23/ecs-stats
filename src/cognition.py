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
                 d.firstname_lastname, d.firstnameen_lastnameen, d.slug, d.profile_image,
                 d.content_published, d.total_read_count
                 FROM author.author d
                 WHERE d.id IN ({})""".format(author_ids)
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
                 AND b.type = 'SYSTEM'
                 AND a.type = 'STORY'
                 AND a.reading_time BETWEEN {} AND {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'])
        cursor.execute(sql)
        record_count = cursor.fetchone()
        total_pratilipis = record_count.get('cnt', 0)
        if total_pratilipis == 0: raise PratilipiNotFound

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
                 AND a.type = 'STORY'
                 AND a.reading_time BETWEEN {} AND {}
                 ORDER BY a.updated_at desc
                 LIMIT {}
                 OFFSET {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'], kwargs['limit'], kwargs['offset'])
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except PratilipiNotFound as err:
        raise PratilipiNotFound
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
                 AND a.type = 'STORY'
                 AND a.reading_time BETWEEN {} AND {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'])
        cursor.execute(sql)
        record_count = cursor.fetchone()
        total_pratilipis = record_count.get('cnt', 0)
        if total_pratilipis == 0: raise PratilipiNotFound

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
                 AND a.type = 'STORY'
                 AND a.reading_time BETWEEN {} AND {}
                 ORDER BY a.reading_time desc
                 LIMIT {}
                 OFFSET {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'], kwargs['limit'], kwargs['offset'])
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except PratilipiNotFound as err:
        raise PratilipiNotFound
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

        sql = """SELECT COUNT(*) as cnt
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
                                              AND b.type = 'SYSTEM'
                                              AND a.type = 'STORY'
                                              AND a.reading_time BETWEEN {} AND {})
                       GROUP BY 1
                       HAVING avg_rating > 3.9
                       AND no_of_rating > 19) AS x""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'])
        cursor.execute(sql)
        record_count = cursor.fetchone()
        total_pratilipis = record_count.get('cnt', 0)
        if total_pratilipis == 0: raise PratilipiNotFound

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
                                               AND b.type = 'SYSTEM'
                                               AND a.type = 'STORY'
                                               AND a.reading_time BETWEEN {} AND {})
                 GROUP BY 1
                 HAVING avg_rating > 3.9
                 AND no_of_rating > 19
                 ORDER BY avg_rating desc, no_of_rating desc
                 LIMIT {}
                 OFFSET {}""".format(kwargs['language'], kwargs['category'], kwargs['from_sec'], kwargs['to_sec'], kwargs['limit'], kwargs['offset'])
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
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except PratilipiNotFound as err:
        raise PratilipiNotFound
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

def get_author_dashboard(kwargs):
    """get author dashboard"""
    try:
        conn = connectdb()
        cursor = conn.cursor()

        author_id = kwargs['author_id']

        # todays and total reads
        sql = """SELECT total_read_count FROM author.author WHERE id = {}""".format(author_id)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        total_read_count = recordset.get('total_read_count', 0)

        # get all pratilipis of an author
        sql = """SELECT id, title, title_en, slug, slug_en, slug_id, cover_image, reading_time, read_count + read_count_offset as read_count
                 FROM pratilipi.pratilipi
                 WHERE author_id = {}
                 AND state = "PUBLISHED"
                 AND content_type IN ('PRATILIPI', 'IMAGE', 'PDF')""".format(author_id)
        cursor.execute(sql)
        pratilipis = cursor.fetchall()
        pratilipiids = ','.join(["'{}'".format(i['id']) for i in pratilipis])

        # total reviews
        sql = """SELECT COUNT(*) as no_of_reviews
                 FROM social.review
                 WHERE reference_type = "PRATILIPI"
                 AND state = "PUBLISHED"
                 AND review != ""
                 AND reference_id IN ({})""".format(pratilipiids)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        total_reviews = recordset.get('no_of_reviews', 0)

        # total followers
        sql = """SELECT COUNT(*) AS no_of_followers
                 FROM follow.follow 
                 WHERE reference_type = "AUTHOR"
                 AND reference_id = '{}'
                 AND state = "FOLLOWING" """.format(author_id)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        total_no_of_followers = recordset.get('no_of_followers', 0)
        
        # todays content published
        sql = """SELECT COUNT(*) as content_published
                 FROM pratilipi.pratilipi
                 WHERE author_id = {}
                 AND state = "PUBLISHED"
                 AND content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND metainfo_updated_at >= convert_tz(CONCAT(SUBSTRING_INDEX(convert_tz(NOW(),@@session.time_zone,'+05:30'), " ", 1), " 00:00:00"),@@session.time_zone,'-05:30')""".format(author_id)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        todays_content_published = recordset.get('content_published', 0)

        # new followers
        sql = """SELECT COUNT(*) AS no_of_followers
                 FROM follow.follow 
                 WHERE reference_type = "AUTHOR"
                 AND reference_id = '{}'
                 AND state = "FOLLOWING"
                 AND date_updated >= convert_tz(CONCAT(SUBSTRING_INDEX(convert_tz(NOW(),@@session.time_zone,'+05:30'), " ", 1), " 00:00:00"),@@session.time_zone,'-05:30')""".format(author_id)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        todays_no_of_followers = recordset.get('no_of_followers', 0)

        # new rating
        sql = """SELECT COUNT(*) as no_of_rating
                 FROM social.review
                 WHERE reference_type = "PRATILIPI" 
                 AND state = 'PUBLISHED' 
                 AND reference_id IN ({})
                 AND date_updated >= convert_tz(CONCAT(SUBSTRING_INDEX(convert_tz(NOW(),@@session.time_zone,'+05:30'), " ", 1), " 00:00:00"),@@session.time_zone,'-05:30')""".format(pratilipiids)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        todays_no_of_rating = recordset.get('no_of_rating', 0)

        # new #reviews
        sql = """SELECT COUNT(*) as no_of_reviews
                 FROM social.review
                 WHERE reference_type = "PRATILIPI"
                 AND state = "PUBLISHED"
                 AND review != ""
                 AND reference_id IN ({})
                 AND date_updated >= convert_tz(CONCAT(SUBSTRING_INDEX(convert_tz(NOW(),@@session.time_zone,'+05:30'), " ", 1), " 00:00:00"),@@session.time_zone,'-05:30')""".format(pratilipiids)
        cursor.execute(sql)
        recordset = cursor.fetchone()
        todays_no_of_reviews = recordset.get('no_of_reviews', 0)

        # most read contents
        sql = """SELECT id, read_count + read_count_offset as read_count
                 FROM pratilipi.pratilipi
                 WHERE author_id = {}
                 AND state = "PUBLISHED"
                 AND content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 ORDER BY 2 desc
                 LIMIT 3""".format(author_id)
        cursor.execute(sql)
        most_read = cursor.fetchall()

        # highest engaged
        sql = """SELECT CAST(reference_id AS SIGNED) as id, COUNT(*) as no_of_reviews
                 FROM social.review 
                 WHERE reference_type = "PRATILIPI"
                 AND state = "PUBLISHED"
                 AND review != ""
                 AND reference_id IN ({})
                 GROUP BY 1
                 ORDER BY 2 DESC 
                 LIMIT 3""".format(pratilipiids)
        cursor.execute(sql)
        highest_engaged = cursor.fetchall()

        # get no_of_review
        sql = """SELECT CAST(reference_id AS SIGNED) as id, COUNT(*) as no_of_reviews
                 FROM social.review
                 WHERE reference_type = "PRATILIPI"
                 AND state = "PUBLISHED"
                 AND review != ""
                 AND reference_id IN ({})
                 GROUP BY 1""".format(pratilipiids)
        cursor.execute(sql)
        pratilipis_review = cursor.fetchall()

        # get no_of_followers 
        sql = """SELECT CAST(reference_id AS SIGNED) as id, ROUND(AVG(rating), 2) as avg_rating
                 FROM social.review
                 WHERE reference_type = "PRATILIPI" 
                 AND state = 'PUBLISHED' 
                 AND reference_id IN ({})
                 GROUP BY 1""".format(pratilipiids)
        cursor.execute(sql)
        pratilipis_rating = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    pratilipi_details = {}
    for i in pratilipis:
        pratilipi_details[i['id']] = i

    review_details = {}
    for i in pratilipis_review:
        review_details[i['id']] = i

    rating_details = {}
    for i in pratilipis_rating:
        rating_details[i['id']] = i

    data = { "total_read_count": total_read_count,
             "total_reviews": total_reviews,
             "total_no_of_followers": total_no_of_followers,
             "todays_no_of_followers": todays_no_of_followers,
             "todays_content_published": todays_content_published,
             "todays_no_of_followers": todays_no_of_followers,
             "todays_no_of_rating": todays_no_of_rating,
             "todays_no_of_reviews": todays_no_of_reviews,
             "pratilipis_review": review_details,
             "pratilipis_rating": rating_details,
             "pratilipis": pratilipi_details,
             "most_read": most_read,
             "highest_engaged": highest_engaged,
           }
    return  data

def get_user_followed_authorIds(user_id):
    try:
        conn = connectdb()
        cursor = conn.cursor()
        sql = """SELECT reference_id FROM follow.follow WHERE user_id={} AND state='FOLLOWING'""".format(user_id)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        author_ids = []
        for i in record_set:
            author_ids.append(i['reference_id'])
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return author_ids

def get_user_feed(user_id, offset):
    limit = 200
    loop_count = 0

    user_following_author_list = []
    pratilipi_published_list = []
    pratilipi_rated_list = []
    user_following_author_list = get_user_following(user_id, limit)
    block_pratilipi_calls = False
    block_rated_pratilipi_calls = False
    print(user_following_author_list)
    if len(user_following_author_list):
        while len(pratilipi_published_list) + len(pratilipi_rated_list) < 10:
            print("loop count is ", loop_count)

            if block_rated_pratilipi_calls and block_pratilipi_calls:
                break

            if len(user_following_author_list) > 0:
                user_following_user_id_list = get_user_id_list_from_athor_ids(user_following_author_list)

                pratilipis = []
                rated_pratilipi = []

                if not block_pratilipi_calls:
                    pratilipis = get_recent_pratilipis_published_by_authors(user_following_author_list, offset)
                    pratilipi_published_list.extend(pratilipis)

                    if len(pratilipis) == 0:
                        block_pratilipi_calls = True
                        print("blocking pratilipi")

                if not block_rated_pratilipi_calls:
                    rated_pratilipi = get_recent_pratilipis_rated_by_authors(user_following_user_id_list, offset)
                    pratilipi_rated_list.extend(rated_pratilipi)

                    if len(rated_pratilipi) == 0:
                        block_rated_pratilipi_calls = True
                        print("blocking rating")

            loop_count = loop_count + 1
            offset = offset + 1

    if len(pratilipi_published_list) + len(pratilipi_rated_list) == 0 :
        raise FeedNotFound

    pratilipi_published_list.extend(pratilipi_rated_list)

    obj_list = [Pratilipi() for i in range(len(pratilipi_published_list))]
    for indx, row in enumerate(pratilipi_published_list):
        for name in row:
            setattr(obj_list[indx], name, row[name])

    return obj_list, offset


def get_user_following(user_id, limit):

    try:
        conn = connectdb()
        cursor = conn.cursor()
        sql = """SELECT reference_id FROM follow.follow WHERE user_id={} AND state='FOLLOWING' LIMIT {}""".format(user_id, limit)
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        author_ids = []
        for i in record_set:
            author_ids.append(int(i['reference_id']))
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return author_ids

def get_user_id_list_from_athor_ids(author_id_list):
    try:
        conn = connectdb()
        cursor = conn.cursor()
        sql = """SELECT user_id FROM author.author WHERE id in {} """.format(tuple(author_id_list))
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        user_ids = []
        for i in record_set:
            user_ids.append(int(i['user_id']))
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return user_ids

def get_recent_pratilipis_published_by_authors(author_list, time_delay):
    try:
        conn = connectdb()
        cursor = conn.cursor()
        day1 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        time_delay = time_delay + 1
        day2 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        sql = """SELECT * FROM pratilipi.pratilipi WHERE author_id in {} AND state='PUBLISHED' and published_at > '{}' and published_at < '{}' """.format(tuple(author_list), day2, day1)
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        pratilipis = []
        for i in record_set:
            pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return pratilipis

def get_recent_pratilipis_rated_by_authors(user_id_list, time_delay):
    try:
        conn = connectdb()
        cursor = conn.cursor()
        day1 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        time_delay = time_delay + 1
        day2 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        sql = """SELECT *, r.rating AS user_rating, r.date_created AS rating_created 
                 FROM pratilipi.pratilipi p 
                 INNER JOIN (
                    SELECT rating, reference_id, date_created
                    FROM social.review 
                    WHERE user_id in {} AND rating > 3 AND state='PUBLISHED' AND reference_type='PRATILIPI' AND date_created > '{}' AND date_created < '{}')
                 AS r ON r.reference_id = p.id;""".format(tuple(user_id_list), day2, day1)
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        pratilipis = []
        for i in record_set:
            pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return pratilipis