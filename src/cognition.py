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

def get_user_feed(user_id, offset, language):
    try:
        limit = 200
        loop_count = 0
        conn = connectdb()
        user_following_author_list = []
        pratilipi_published_list = []
        pratilipi_rated_list = []
        user_following_author_list = get_user_following(user_id, limit, conn)
        block_pratilipi_calls = False
        block_rated_pratilipi_calls = False
        print(user_following_author_list)
        if len(user_following_author_list) > 0:
            while len(pratilipi_published_list) + len(pratilipi_rated_list) < 10:

                if block_rated_pratilipi_calls and block_pratilipi_calls:
                    break

                if len(user_following_author_list) > 0:
                    user_following_user_id_list = get_user_id_list_from_athor_ids(user_following_author_list, conn)

                    pratilipis = []
                    rated_pratilipi = []

                    pratilipis = get_recent_pratilipis_published_by_authors(user_following_author_list, offset, conn)
                    pratilipi_published_list.extend(pratilipis)

                    if len(pratilipis) == 0:
                        block_pratilipi_calls = True

                    rated_pratilipi = get_recent_pratilipis_rated_by_authors(user_following_user_id_list, offset, conn)
                    pratilipi_rated_list.extend(rated_pratilipi)

                    if len(rated_pratilipi) == 0:
                        block_rated_pratilipi_calls = True

                loop_count = loop_count + 1
                offset = offset + 1

        if len(pratilipi_published_list) + len(pratilipi_rated_list) == 0:
            pratilipi_published_list.extend(get_default_feed(offset, conn, language))
            offset = offset + 1

        pratilipi_published_list.extend(pratilipi_rated_list)
        pratilipi_published_list = pratilipi_published_list[:30]

        obj_list = [Pratilipi() for i in range(len(pratilipi_published_list))]
        for indx, row in enumerate(pratilipi_published_list):
            for name in row:
                setattr(obj_list[indx], name, row[name])

        return obj_list, offset
    except Exception as err:
        raise FeedNotFound
    finally:
        disconnectdb(conn)


def get_default_feed(time_delay, conn, language):
    pratilipis = []
    try:
        cursor = conn.cursor()
        day1 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        time_delay = time_delay + 1
        day2 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        sql = """SELECT *, True as is_default  FROM pratilipi.pratilipi 
        WHERE state='PUBLISHED' and language='{}' and published_at > '{}' and published_at < '{}' 
        order by read_count desc limit 10""".format(language, day2, day1)
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)

    return pratilipis


def get_user_following(user_id, limit, conn):
    author_ids = []
    try:
        cursor = conn.cursor()
        sql = """SELECT reference_id FROM follow.follow WHERE user_id={} AND state='FOLLOWING' LIMIT {}""".format(user_id, limit)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            author_ids.append(int(i['reference_id']))
    except Exception as err:
        raise DbSelectError(err)

    return author_ids

def get_user_id_list_from_athor_ids(author_id_list, conn):
    user_ids = []
    try:
        cursor = conn.cursor()
        sql = """SELECT user_id FROM author.author WHERE id in {} """.format(tuple(author_id_list))
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            user_ids.append(int(i['user_id']))
    except Exception as err:
        raise DbSelectError(err)

    return user_ids

def get_recent_pratilipis_published_by_authors(author_list, time_delay, conn):
    pratilipis = []

    try:
        cursor = conn.cursor()
        day1 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        time_delay = time_delay + 1
        day2 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        sql = """SELECT * FROM pratilipi.pratilipi WHERE author_id in {} AND state='PUBLISHED' and published_at > '{}' and published_at < '{}' """.format(tuple(author_list), day2, day1)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)

    return pratilipis

def get_recent_pratilipis_rated_by_authors(user_id_list, time_delay, conn):
    pratilipis = []

    try:
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
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)

    return pratilipis

def get_top_authors(language):
    try:
        conn = connectdb()
        cursor = conn.cursor()
        startday = (datetime.now() + timedelta(days=-7)).strftime("%Y-%m-%d")
        sql = """SELECT author.first_name, author.first_name_en, author.last_name, author.last_name_en, author.pen_name, author.pen_name_en,
                author.firstname_lastname, author.firstnameen_lastnameen, author.slug, author.profile_image,
                author.content_published, author.total_read_count,
                a.author_id, a.avg_read,
                a.total_read,
                SUM(b.rating_count) as total_rating,
                SUM(b.rating_count) /COUNT(b.pratilipi_id) as average_rating_count,
                SUM(b.average_rating)/COUNT(b.pratilipi_id) AS average_rate,
                (b.rating_count / a.total_read * 100 ) AS rate_read_ratio,
               a.total_content_published
               FROM
                   author.author AS author,
                   (SELECT author_id, read_count, id, SUM(read_count) / COUNT(DISTINCT id) AS avg_read,
                   COUNT(DISTINCT id) AS total_content_published,
                   SUM(read_count) AS total_read
                       FROM pratilipi.pratilipi
                       WHERE state = "PUBLISHED" AND published_at > '{}' AND language = '{}' GROUP BY author_id) AS a,
                       (SELECT SUM(a.rating)/COUNT(a.user_id) AS average_rating,
                           COUNT(a.user_id) AS rating_count, a.reference_id AS pratilipi_id, b.author_id
                           FROM social.review AS a,
                       (SELECT id, author_id
                           FROM pratilipi.pratilipi
                           WHERE state = "PUBLISHED" AND published_at > '{}' AND language = '{}')
                           AS b
                               WHERE a.reference_id = b.id GROUP BY a.reference_id) AS b
                   WHERE a.author_id = b.author_id AND a.total_read > 100 AND a.author_id = author.id
                   GROUP BY a.author_id
                   HAVING SUM(b.rating_count) /COUNT(b.pratilipi_id) > 5
                   ORDER BY average_rate DESC LIMIT 20;""".format(startday, language, startday, language)
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    obj_list = [ ]
    for i in record_set:
        obj_list.append(i)
    return obj_list



def get_most_active_authors_list(language, time_delay, offset):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        day2 = (datetime.now()).strftime("%Y-%m-%d")
        day1 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")

        sql = """ SELECT author_id, count(*) as rank FROM pratilipi.pratilipi
            where language='{}' AND state='PUBLISHED' AND published_at > '{}' AND published_at < '{}'
            group by author_id order by rank desc limit 20 offset {}""".format(language, day1, day2, offset)

        cursor.execute(sql)
        record_set = cursor.fetchall()
        author_ids = []
        for i in record_set:
            author_ids.append(i['author_id'])

    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return author_ids

def get_reader_score(kwargs):
    """get reader score"""
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT SUM(property_value) as word_count
                 FROM user_pratilipi.user_pratilipi
                 WHERE user_id = {}
                 AND property = 'READ_WORD_COUNT'""".format(kwargs['user_id'])
        cursor.execute(sql)
        word_count = cursor.fetchone()
        word_count = word_count.get('word_count', 0)
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    if word_count == 0 or word_count is None:
        return 0, None, None

    word_count = int(word_count)

    no_words_for_one_book = 20000
    no_of_books_read = None

    if word_count > 4096000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 2048000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 1024000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 512000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 256000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 112000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 56000:
        no_of_books_read = word_count/no_words_for_one_book
    elif word_count > 28000:
        no_of_books_read = word_count/no_words_for_one_book

    tier = None
    if word_count >= 512000 and word_count <= 1024000:
        # top 10%
        tier = "10%"
    elif word_count >= 1025000 and word_count <= 2048000:
        # top 5%
        tier = "5%"
    elif word_count >= 2049000:
        # top 1%
        tier = "1%"

    return word_count, no_of_books_read, tier
