#!/usr/bin/env python
# -*- coding: utf-8 -*-

import __builtin__
import json

from itertools import islice
from model import *
from exceptions import *
from dbutil import *
from redisutil import *

# hindi, bengali, gujurati, tamil, telugu, kannada
uni_array = [u'०', u'१' , u'२', u'३', u'४', u'५', u'६', u'७', u'८', u'९',
             u'০', u'১', u'২', u'৩', u'৪', u'৫', u'৬', u'৭', u'৮', u'৯',
             u'૦', u'૧', u'૨', u'૩', u'૪', u'૫', u'૬', u'૭', u'૮', u'૯',
             u'௦', u'௧', u'௨', u'௩', u'௪', u'௫', u'௬', u'௭', u'௮', u'௯',
             u'౦', u'౧', u'౨',	u'౩', u'౪',	u'౫', u'౬',	u'౭', u'౮', u'౯',
             u'೦', u'೧', u'೨', u'೩', u'೪', u'೫', u'೬', u'೭', u'೮', u'೯',
             u'൦', u'൧', u'൨', u'൩', u'൪',	u'൫', u'൬', u'൭', u'൮', u'൯']


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

        sql = """SELECT reference_id as id, AVG(rating) as avg_rating, date_created
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

def get_user_ratings(user_id, pratilipi_ids):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT reference_id as id, rating, date_created
                 FROM social.review
                 WHERE reference_type = 'PRATILIPI'
                 AND user_id = {}
                 AND state = 'PUBLISHED'
                 AND reference_id IN ({})""".format(user_id, pratilipi_ids)
        cursor.execute(sql)
        record_set = cursor.fetchall()
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)

    return record_set

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

def get_authors_for_feed(author_ids, user_ids):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        if len(author_ids) > 0 and len(user_ids) > 0:
            sql = """SELECT d.id, d.user_id, d.first_name, d.first_name_en, d.last_name, d.last_name_en, d.pen_name, d.pen_name_en,
                     d.firstname_lastname, d.firstnameen_lastnameen, d.slug, d.profile_image,
                     d.content_published, d.total_read_count
                     FROM author.author d
                     WHERE d.id IN ({}) or d.user_id in ({})""".format(author_ids, user_ids)
        elif len(author_ids) > 0:
            sql = """SELECT d.id, d.user_id, d.first_name, d.first_name_en, d.last_name, d.last_name_en, d.pen_name, d.pen_name_en,
                                 d.firstname_lastname, d.firstnameen_lastnameen, d.slug, d.profile_image,
                                 d.content_published, d.total_read_count
                                 FROM author.author d
                                 WHERE d.id IN ({})""".format(author_ids)
        else:
            sql = """SELECT d.id, d.user_id, d.first_name, d.first_name_en, d.last_name, d.last_name_en, d.pen_name, d.pen_name_en,
                                 d.firstname_lastname, d.firstnameen_lastnameen, d.slug, d.profile_image,
                                 d.content_published, d.total_read_count
                                 FROM author.author d
                                 WHERE d.user_id in ({})""".format(user_ids)
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
        conn = connectdb()
        cursor = conn.cursor()
        user_following_author_id_list, user_following_user_id_list = get_user_following(user_id, limit, conn)
        print(user_following_author_id_list, user_following_user_id_list)

        if len(user_following_author_id_list) > 0:
            author_ids = ",".join(user_following_author_id_list)
            author_user_ids = ",".join(user_following_user_id_list)

            sql = """SELECT * FROM experiment.user_activity
                WHERE (author_id IN ({})
                AND activity_type = 'PUBLISHED' )
                OR (activity_initiated_by IN ({})
                AND activity_type = 'RATED' ) ORDER BY activity_performed_at DESC LIMIT 20 OFFSET {};
            """.format(author_ids, author_user_ids, offset)
            print(sql)
            cursor.execute(sql)
            record_set = cursor.fetchall()


            offset = offset + 20
            return record_set, offset
        else:

            if offset/10 > 8:
                return [], 90

            def_feed = get_default_from_redis(offset/10, language)
            if len(def_feed) == 0:
                def_feed = get_default_feed(offset/10, conn, language)
                add_data_to_redis(offset/10, language, def_feed)

            return def_feed, offset + 10
    except Exception as err:
        raise err
    finally:
        disconnectdb(conn)


def get_default_from_redis(day, language):
    try:
        conn = connect_redis()
        name = "FEED_GENERIC_{}".format(day)
        feed_data = conn.hget(name, language)
        response = []
        if feed_data:
            response = json.loads(feed_data)
    except Exception as err:
        raise RedisConnectionError(err)
    finally:
        disconnect_redis(conn)

    return response

def add_data_to_redis(day, language, value):
    try:
        conn = connect_redis()
        name = "FEED_GENERIC_{}".format(day)
        conn.hset(name, language, json.dumps(value))
        ttl = datetime.today() + timedelta(hours=12)
        conn.expireat(name=name, when=ttl)
    except Exception as err:
        raise RedisConnectionError(err)
    finally:
        disconnect_redis(conn)

def get_default_feed(time_delay, conn, language):
    pratilipis = []
    try:
        cursor = conn.cursor()
        day1 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        time_delay = time_delay + 1
        day2 = (datetime.now() + timedelta(days=-time_delay)).strftime("%Y-%m-%d")
        sql = """SELECT id as activity_reference_id, user_id, author_id, 'PUBLISHED' as activity_type FROM pratilipi.pratilipi
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
    author_user_ids = []
    try:
        cursor = conn.cursor()
        sql = """SELECT user_id, id as author_id FROM author.author as a
         JOIN (SELECT reference_id FROM follow.follow WHERE user_id={} AND state='FOLLOWING' LIMIT {}) as f on a.id = f.reference_id""".format(user_id, limit)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            author_ids.append(str(i['author_id']))
            author_user_ids.append(str(i['user_id']))
    except Exception as err:
        raise DbSelectError(err)

    return author_ids, author_user_ids

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

def get_pratilipis(pratilipi_id_list):
    pratilipis = []

    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT * FROM pratilipi.pratilipi
        WHERE id in ({})
        AND state='PUBLISHED'
        AND NOT content_type = 'AUDIO'
         """.format(pratilipi_id_list)
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)

    return pratilipis

def get_pratilipis_for_you(pratilipi_id_list, user_id, language):
    pratilipis = []

    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql = """SELECT * FROM pratilipi.pratilipi
        WHERE id in ({})
        AND state='PUBLISHED'
        AND NOT content_type IN ('AUDIO')
        AND type NOT IN ('POEM', 'ARTICLE')
        AND title_en not like '%Untitled%'
        AND language = '{}'
        AND user_id != {}
        AND read_count > 200
         """.format(pratilipi_id_list, language, user_id)
        print(sql)
        cursor.execute(sql)
        record_set = cursor.fetchall()
        for i in record_set:
            if is_not_serialized(i):
                pratilipis.append(i)
    except Exception as err:
        raise DbSelectError(err)

    return pratilipis


def get_top_authors(language, period, offset, limit):
    try:
        conn = connect_redis()

        obj_list = []
        for rank in range(offset, offset + limit):
            author_data = conn.hget('ecsstats:top_authors:authors:{}:{}'.format(language, period), rank)
            if author_data == None:
                break
            obj_list.append(json.loads(author_data))

    except Exception as err:
        raise RedisConnectionError(err)
    finally:
        disconnect_redis(conn)

    return obj_list

def get_top_author_rank(language, period, user_id):
    try:
        conn = connect_redis()
        user_rank_json = conn.hget('ecsstats:top_authors:ranks:{}:{}'.format(language, period), user_id)
        print(user_id)
        print(user_rank_json)
        user_rank_data = None
        if user_rank_json != None:
            user_rank_data = json.loads(user_rank_json)

    except Exception as err:
        raise RedisConnectionError(err)
    finally:
        disconnect_redis(conn)

    return user_rank_data

def get_author_leaderboard(language, period, offset, limit):
    try:
        conn = connect_redis()

        obj_list = []
        for rank in range(offset, offset + limit):
            author_data = conn.hget('ecsstats:author_leaderboard:authors:{}:{}'.format(language, period), rank)
            if author_data == None:
                break
            obj_list.append(json.loads(author_data))

    except Exception as err:
        raise RedisConnectionError(err)
    finally:
        disconnect_redis(conn)

    return obj_list

def get_author_leaderboard_rank(language, period, user_id):
    try:
        conn = connect_redis()
        user_rank_json = conn.hget('ecsstats:author_leaderboard:ranks:{}:{}'.format(language, period), user_id)
        print(user_id)
        print(user_rank_json)
        user_rank_data = None
        if user_rank_json != None:
            user_rank_data = json.loads(user_rank_json)

    except Exception as err:
        raise RedisConnectionError(err)
    finally:
        disconnect_redis(conn)

    return user_rank_data


def get_most_active_authors_list(language, offset):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        day2 = (datetime.now()).strftime("%Y-%m-%d")
        day1 = (datetime.now() + timedelta(days=-7)).strftime("%Y-%m-%d")

        sql = """ SELECT author_id, count(*) as rank FROM pratilipi.pratilipi
            where language='{}' AND state='PUBLISHED' AND reading_time > 60 AND published_at > '{}' AND published_at < '{}'
            group by author_id order by rank desc limit 20""".format(language, day1, day2)

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

# def get_most_active_authors_list(language, offset):
#     try:
#         conn = connect_redis()
#         name = "MOST_ACTIVE"
#         feed_data = conn.hget(name, language)
#         response = []
#         if feed_data:
#             response = json.loads(feed_data)
#     except Exception as err:
#         raise RedisConnectionError(err)
#     finally:
#         disconnect_redis(conn)
#
#     return response

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

def get_continue_reading(kwargs):
    """get continue reading"""
    try:
        conn = __builtin__.CONN_RO
        cursor = conn.cursor()

        # fetch data
        user_id = kwargs['user_id']
        limit = kwargs['limit']
        offset = kwargs['offset']
        total_pratilipis = 0

        # get pratilipis added to library
        sql = """SELECT c.id, c.author_id, c.content_type, c.cover_image, c.language, c.type,
                 c.read_count_offset + c.read_count as read_count,
                 c.title, c.title_en, c.slug, c.slug_en, c.slug_id, c.reading_time, c.updated_at,
                 d.property_value*60*100/c.reading_time as reading_percentage
                 FROM library.library a, library.resource b, pratilipi.pratilipi c, user_pratilipi.user_pratilipi d
                 WHERE a.id = b.library_id
                 AND b.reference_id = c.id
                 AND b.reference_id = d.pratilipi_id
                 AND a.user_id = d.user_id
                 AND a.state = 'ACTIVE'
                 AND a.user_id = {}
                 AND b.reference_type = 'PRATILIPI'
                 AND b.state = 'ADDED'
                 AND b.date_updated BETWEEN CURRENT_TIMESTAMP() - INTERVAL 60 DAY AND CURRENT_TIMESTAMP() - INTERVAL 1 DAY
                 AND c.state = 'PUBLISHED'
                 AND c.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND d.user_id = {}
                 AND d.property = 'READ_WORD_COUNT'""".format(user_id, user_id)
        cursor.execute(sql)
        library_set = cursor.fetchall()
        total_pratilipis = cursor.rowcount

        # get pratilipis read by user
        sql = """SELECT b.id, b.author_id, b.content_type, b.cover_image, b.language, b.type,
                 b.read_count_offset + b.read_count as read_count,
                 b.title, b.title_en, b.slug, b.slug_en, b.slug_id, b.reading_time, b.updated_at,
                 a.property_value*60*100/b.reading_time as reading_percentage
                 FROM user_pratilipi.user_pratilipi a, pratilipi.pratilipi b
                 WHERE a.pratilipi_id = b.id
                 AND a.property = 'READ_WORD_COUNT'
                 AND a.property_value > 800
                 AND a.updated_at BETWEEN CURRENT_TIMESTAMP() - INTERVAL 30 DAY AND CURRENT_TIMESTAMP() - INTERVAL 1 DAY
                 AND a.user_id = {}
                 AND b.state = 'PUBLISHED'
                 AND b.content_type IN ('PRATILIPI', 'IMAGE', 'PDF')
                 AND b.reading_time > 0
                 AND a.property_value*60*100/b.reading_time BETWEEN 50 AND 90""".format(user_id)
        cursor.execute(sql)
        read_set = cursor.fetchall()
        total_pratilipis = total_pratilipis + cursor.rowcount

        if total_pratilipis == 0: raise NoDataFound("nothing in library and read history")

        # get avg rating for selected pratilipis
        temp = []
        for i in read_set: temp.append(str(i['id']))
        pratilipiids = ','.join(temp)

        rating_set = []
        if len(temp) > 0:
            sql = """SELECT reference_id as id, AVG(rating) as avg_rating
                     FROM social.review
                     WHERE reference_type = 'PRATILIPI'
                     AND state = 'PUBLISHED'
                     AND reference_id IN ({})
                     GROUP BY 1
                     HAVING avg_rating > 3.5""".format(pratilipiids)
            cursor.execute(sql)
            rating_set = cursor.fetchall()
    except PratilipiNotFound as err:
        raise PratilipiNotFound
    except NoDataFound as err:
        raise NoDataFound(err)
    except Exception as err:
        raise DbSelectError(err)
    finally:
        cursor.close()

    # apply avg_rating filter
    rating_list = []
    for i in rating_set: rating_list.append(int(i['id']))

    library_pratilipis = {}
    for i in library_set:
        rp = i['reading_percentage'] if i['reading_percentage'] <= 100 else 100.0
        k = "{}-{}".format(rp, i['id'])
        library_pratilipis[k] = i

    read_pratilipis = {}
    for i in read_set:
        if i['id'] not in rating_list: continue
        rp = i['reading_percentage'] if i['reading_percentage'] <= 100 else 100.0
        k = "{}-{}".format(rp, i['id'])
        read_pratilipis[k] = i

    if len(library_pratilipis) == 0 and len(read_pratilipis) == 0: raise NoDataFound("no pratilipi found after avg rating filter")

    # order data
    all_pratilipis = []
    lib_keys = library_pratilipis.keys()
    lib_keys.sort()
    for i in reversed(lib_keys):
        all_pratilipis.append(library_pratilipis[i])

    read_keys = read_pratilipis.keys()
    read_keys.sort()
    for i in reversed(read_keys):
        # avoid dups
        if i in library_pratilipis:
            continue
        all_pratilipis.append(read_pratilipis[i])

    # slice data
    sliced_list = list(islice(islice(all_pratilipis, offset, None), limit))

    if len(sliced_list) == 0: raise NoDataFound("no pratilipi found after limit and offset")

    # prepare list of objects
    obj_list = [ Pratilipi() for i in range(len(sliced_list)) ]
    for indx, row in enumerate(sliced_list):
        for name in row:
            setattr(obj_list[indx], name, row[name])
    return obj_list, total_pratilipis

def get_reader_dashboard_stats(user_id):
    try:
        conn = connectdb()
        cursor = conn.cursor()

        sql_for_basic_stats = """ SELECT
                    read_stats.word_count as word_count,
                    read_stats.pratilipi_count as pratilipi_count,
                    review_stats.only_review as only_reviews,
                    review_stats.rate_and_review as rate_and_review,
                    following_stats.following_count as following_count
                    FROM
                        (SELECT
                            SUM(property_value) as word_count,
                            COUNT(DISTINCT pratilipi_id) as pratilipi_count
                            FROM user_pratilipi.user_pratilipi
                            WHERE property = 'READ_WORD_COUNT' AND user_id = {}) as read_stats,
                        (SELECT
                            SUM(CASE WHEN review != "" THEN 1 ELSE 0 END) AS only_review,
                            COUNT(DISTINCT id) AS rate_and_review
                            FROM    social.review
                            WHERE user_id={}) as review_stats,
                        (SELECT
                            COUNT(DISTINCT id) AS following_count
                            FROM    follow.follow
                            WHERE user_id={} AND state = 'FOLLOWING') as following_stats;""".format(user_id, user_id, user_id)

        cursor.execute(sql_for_basic_stats)
        record_set = cursor.fetchall()
        if cursor.rowcount == 0: raise NoDataFound("No user found with the given id")

        stats = {
            'word_count': record_set[0]['word_count'],
            'pratilipi_count': record_set[0]['pratilipi_count'],
            'only_reviews': record_set[0]['only_reviews'],
            'rate_and_review': record_set[0]['rate_and_review'],
            'following_count': record_set[0]['following_count']
        }

        sql_for_reading_tags = """ SELECT COUNT(category_id) as frequency, category_id, categories.name as name
                                    FROM pratilipi.pratilipis_categories
                                	JOIN pratilipi.categories categories
                                    ON categories.id = category_id
                                    WHERE pratilipi_id IN
                                		(SELECT DISTINCT pratilipi_id
                                			FROM user_pratilipi.user_pratilipi
                                			WHERE user_id = {})
                                	GROUP BY category_id
                                    ORDER BY COUNT(category_id) DESC;""".format(user_id)

        cursor.execute(sql_for_reading_tags)
        category_data = cursor.fetchall()
        read_categories = []

        for i in category_data:
            category_data = {}
            category_data['frequency'] = int(i['frequency'])
            category_data['category_id'] = i['category_id']
            category_data['name'] = i['name']
            read_categories.append(category_data)

        stats['read_categories'] = read_categories[:3]

        sql_for_dashboard_privacy = """ SELECT * FROM user.preference
                                        WHERE user_id = {} AND type = '{}'""".format(user_id, 'READER_DASHBOARD_PRIVACY')
        cursor.execute(sql_for_dashboard_privacy)
        privacy_data = cursor.fetchall()

        if cursor.rowcount == 0:
            stats['is_private'] = False
        else:
            if privacy_data[0]['value'] == 'PRIVATE':
                stats['is_private'] = True
            else:
                stats['is_private'] = False

    except NoDataFound as err:
        raise NoDataFound(err)
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)
    return stats


def get_for_you(user_id, offset):
    try:
        offset_array = offset.split("-")
        offset = int(offset_array[0]) if int(offset_array[0]) > 0 else 0
        offset_similarity = int(offset_array[1]) if int(offset_array[1]) > 0 else 0

        conn = connectdb()
        cursor = conn.cursor()

        conn_ds = connect_datascience_db()
        cursor_ds = conn_ds.cursor()

        # get user read pratilipi sort by time get latest 10
        # get similar pratilipi for 10 pratilipis each 5
        # filter already read
        # rate with SVD server highest rating
        sql = """SELECT pratilipi_id from user_pratilipi.user_pratilipi
                where user_id = {}
                and property='READ_WORD_COUNT'
                and property_value > 200
                order by updated_at limit 10 offset {}""".format(user_id, offset)

        cursor.execute(sql)
        record_set = cursor.fetchall()

        if len(record_set) == 0:
            if offset == 0 and offset_similarity == 0:
                # user hasn't read anything yet
                return []
            elif offset > 0:
                # used up all pratilipis read by user with 3 highest similar
                offset = 0
                offset_similarity = offset_similarity + 3

            sql = """SELECT pratilipi_id from user_pratilipi.user_pratilipi
                            where user_id = {}
                            and property='READ_WORD_COUNT'
                            and property_value > 200
                            order by updated_at limit 10 offset {}""".format(user_id, offset)

            cursor.execute(sql)
            record_set = cursor.fetchall()


        pratilipi_similarity = []
        for x in record_set:
            sql = """ SELECT * FROM similarity.pratilipi_similarity
                    where pratilipi_1 = {}
                    OR pratilipi_2 = {}
                    order by similarity desc limit 3 offset {}""".format(x['pratilipi_id'], x['pratilipi_id'], offset_similarity)
            print(sql)
            cursor_ds.execute(sql)
            record_set = cursor_ds.fetchall()
            pratilipi_similarity.extend(record_set)

        offset = offset + 10
        return pratilipi_similarity, offset, offset_similarity
    except NoDataFound as err:
        raise NoDataFound(err)
    except Exception as err:
        raise DbSelectError(err)
    finally:
        disconnectdb(conn)


def is_not_serialized(pratilipi):
    for x in uni_array:
        if pratilipi['title'].find(x) >= 0:
            return False
    return True
