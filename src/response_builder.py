import json
import os
from datetime import datetime
from commonfns import timeit
from pprint import pprint as p
import supporting_services as supp_service
from static import  translations
def _set_key(d, k, v):
    """set dict key if its value is not None"""
    if v is not None:
        d[k] = v
    return d

def _author_name(author):
    """advance name details"""
    response = {}
    name = ' '.join(filter(None, (author['first_name'], author['last_name'])))
    response = _set_key(response, 'name', name if name.__len__() > 0 else None)

    name = ' '.join(filter(None, (author['first_name_en'], author['last_name_en'])))
    response = _set_key(response, 'nameEn', name if name.__len__() > 0 else None)

    name = ' '.join(filter(None, (author['first_name'], author['last_name'])))
    name = ' '.join(filter(None, (name, '"{}"'.format(author['pen_name']) if author['pen_name'] is not None and len(author['pen_name']) >0 else None)))
    response = _set_key(response, 'fullName', name)

    name = ' '.join(filter(None, (author['first_name_en'], author['last_name_en'])))
    name = ' '.join(filter(None, (name, '"{}"'.format(author['pen_name_en'] if author['pen_name_en'] is not None and len(author['pen_name_en']) >0 else None))))
    response = _set_key(response, 'fullNameEn', name)

    response = _set_key(response, 'displayName', response['fullName'] if response['fullName'] != '' else response['fullNameEn'])
    return response['displayName']

def _author_slug_details(author):
    """slug details"""
    response = {}
    response = _set_key(response, 'pageUrl', '/user/{}-{}'.format(author['firstname_lastname'], author['slug']))
    return response['pageUrl']

def _pratilipi_cover_image(pratilipi_id, cover_image):
    pratilipi_id = int(pratilipi_id)
    sub_domain_number = pratilipi_id % 5 if cover_image is not None else 0
    prefix = 'https://{}.ptlp.co'.format(sub_domain_number)
    suffix = '/pratilipi/cover?pratilipiId={}&version={}'.format(pratilipi_id, cover_image) if cover_image is not None else '/pratilipi/cover'
    return "{}{}".format(prefix,suffix)

def _pratilipi_details(pratilipi, author, rating, add_to_lib):
    """pratilipi details"""
    response = {}
    response = _set_key(response, 'pratilipiId', pratilipi.id)
    response = _set_key(response, 'language', pratilipi.language)
    response = _set_key(response, 'displayTitle', pratilipi.title if pratilipi.title != '' else pratilipi.title_en)
    response = _set_key(response, 'readCount', pratilipi.read_count)

    pratilipi_slug = pratilipi.slug if pratilipi.slug != '' else pratilipi.slug_en
    response = _set_key(response, 'pageUrl', '/story/{}-{}'.format(pratilipi_slug, pratilipi.slug_id))
    response = _set_key(response, 'slug', response['pageUrl'])

    response = _set_key(response, 'readingTime', pratilipi.reading_time)
    response = _set_key(response, 'type', pratilipi.type)
    response = _set_key(response, 'contentType', pratilipi.content_type)
    response = _set_key(response, 'lastUpdatedDateMillis', int(pratilipi.updated_at.strftime("%s")) * 1000)

    response = _set_key(response, 'coverImageUrl', _pratilipi_cover_image(pratilipi.id, pratilipi.cover_image))
    response = _set_key(response, 'averageRating', "{0:.2f}".format(rating))
    #response = _set_key(response, 'addToLib', add_to_lib)

    data = {}
    data['authorId'] = pratilipi.author_id
    data['displayName'] = _author_name(author)
    data['pageUrl'] = _author_slug_details(author)
    data['slug'] = _author_slug_details(author)

    response = _set_key(response, 'author', data)
    return response

def for_OK():
    """for OK response"""
    response = {}
    response = _set_key(response, 'message', 'OK')
    return json.dumps(response)

def for_ping(data):
    """for ping response"""
    response = {}
    response = _set_key(response, 'message', datetime.strftime(data.dt, '%Y-%m-%d %H:%M:%S'))
    return json.dumps(response)

def for_all(kwargs):
    """for all response"""
    pratilipis = kwargs['pratilipis']
    authors = kwargs['authors']
    ratings = kwargs['ratings']
    librarys = kwargs['librarys']

    response = {}
    response = _set_key(response, 'found', kwargs['total_pratilipis'])
    response = _set_key(response, 'limit', kwargs['limit'])
    response = _set_key(response, 'offset', kwargs['offset'])
    response = _set_key(response, 'pratilipiList', [])
    for pratilipi in pratilipis:
        #add_to_lib = True if librarys.get(pratilipi.id, None) is None else False
        add_to_lib = False
        rating = ratings[str(pratilipi.id)]['avg_rating'] if str(pratilipi.id) in ratings else 0
        data = _pratilipi_details(pratilipi, authors[pratilipi.author_id], rating, add_to_lib)
        response['pratilipiList'].append(data)
    return json.dumps(response)

def for_author_dashboard(kwargs):
    """for author dashboard"""
    pratilipis = kwargs['pratilipis']
    pratilipis_rating = kwargs['pratilipis_rating']
    pratilipis_review = kwargs['pratilipis_review']

    response = {}
    temp = { 'readCount': kwargs['total_read_count'],
            'follower': kwargs['total_no_of_followers'],
            'reviewCount': kwargs['total_reviews'],
            'highestRating': 0 }
    response = _set_key(response, 'total', temp)

    temp = { 'contentPublished': kwargs['todays_content_published'],
             'follower': kwargs['todays_no_of_followers'],
             'readCount': kwargs['total_read_count'],
             'reviewCount': kwargs['todays_no_of_reviews'],
             'ratingCount': kwargs['todays_no_of_rating'] }
    response = _set_key(response, 'todays', temp)

    response = _set_key(response, 'highestReviewedPratilipi', [])
    response = _set_key(response, 'highestReadCountPratilipi', [])

    highest_rating = 0

    for pratilipi in kwargs['most_read']:
        pid = pratilipi['id']
        rating = pratilipis_rating.get(pid, None)
        rating = pratilipis_rating[pid]['avg_rating'] if rating is not None else 0
        review = pratilipis_review.get(pid, None)
        review = pratilipis_review[pid]['no_of_reviews'] if review is not None else 0

        temp = { 'pratilipiId': pid,
                 'readingTime': pratilipis[pid]['reading_time'],
                 'readCount': pratilipi['read_count'],
                 'displayTitle': pratilipis[pid]['title'] if pratilipis[pid]['title'] != '' else pratilipis[pid]['title_en'],
                 'pageUrl': '/story/{}-{}'.format(pratilipis[pid]['slug'], pratilipis[pid]['slug_id']),
                 'coverImageUrl': _pratilipi_cover_image(pid, pratilipis[pid]['cover_image']),
                 'avgRating': rating,
                 'reviewCount': review,
               }
        response['highestReadCountPratilipi'].append(temp)
        highest_rating = float(highest_rating) + float(temp['avgRating'])

    for pratilipi in kwargs['highest_engaged']:
        pid = pratilipi['id']
        rating = pratilipis_rating.get(pid, None)
        rating = pratilipis_rating[pid]['avg_rating'] if rating is not None else 0
        review = pratilipis_review.get(pid, None)
        review = pratilipis_review[pid]['no_of_reviews'] if review is not None else 0

        temp = { 'pratilipiId': pid,
                 'readingTime': pratilipis[pid]['reading_time'],
                 'readCount': pratilipis[pid]['read_count'],
                 'displayTitle': pratilipis[pid]['title'] if pratilipis[pid]['title'] != '' else pratilipis[pid]['title_en'],
                 'pageUrl': '/story/{}-{}'.format(pratilipis[pid]['slug'], pratilipis[pid]['slug_id']),
                 'coverImageUrl': _pratilipi_cover_image(pid, pratilipis[pid]['cover_image']),
                 'avgRating': rating,
                 'reviewCount': review,
               }
        response['highestReviewedPratilipi'].append(temp)
        highest_rating = float(highest_rating) + float(temp['avgRating'])

    response['total']['highestRating'] = "{0:.2f}".format(highest_rating/(len(response['highestReviewedPratilipi']) + len(response['highestReadCountPratilipi'])))
    return json.dumps(response)

def for_author_recommendations(kwargs):
    """author recommendations"""
    response_dict = {'authorList': []}
    authors = kwargs['authors']
    bucket = None
    cursor = None
    logged_user_id = kwargs['logged_user_id']

    if kwargs.has_key('cursor'):
        cursor = kwargs['cursor']
    if kwargs.has_key('bucket'):
        bucket = kwargs['bucket']

    for author in authors:
        response = {}
        response = _set_key(response, 'authorId', author.id)
        response = _set_key(response, 'firstName', author.first_name)
        response = _set_key(response, 'name', author.first_name)
        response = _set_key(response, 'contentPublished', author.content_published)
        response = _set_key(response, 'totalReadCount', author.total_read_count)
        response = _set_key(response, 'profileImageUrl', supp_service.get_image_url(author.id, author.profile_image, 'image'))

        data = supp_service.follow_details([author.id], [logged_user_id], logged_user_id)
        response = _set_key(response, 'following', False)
        response = _set_key(response, 'followCount', data[author.id]['followersCount'] if data != {} else 0)
        response_dict['authorList'].append(response)

    meta = {}

    if bucket is not None:
        meta['algorithmId'] = bucket
    if cursor is not None:
        response_dict['cursor'] = str(20 + int(cursor))

    response_dict['meta'] = meta
    return json.dumps(response_dict)

def for_user_feed(kwargs):
    pratilipis = kwargs['pratilipis']
    authors = kwargs['authors']
    ratings = kwargs['ratings']
    feed_list = kwargs['feed_pratilipi_list']
    response_dict = { "feedList":[]}

    for feed in feed_list:
        if feed['activity_reference_id'] in pratilipis:
            pratilipi = pratilipis[feed['activity_reference_id']]
            rating = ratings[str(pratilipi['id'])]['avg_rating'] if str(pratilipi['id']) in ratings else 0
            author = authors[pratilipi['author_id']]
            response_object = {}
            response_pratilipi = {}
            response_pratilipi = _set_key(response_pratilipi, 'pratilipiId', pratilipi['id'])
            response_pratilipi = _set_key(response_pratilipi, 'title', pratilipi['title'])
            response_pratilipi = _set_key(response_pratilipi, 'titleEn', pratilipi['title_en'])
            response_pratilipi = _set_key(response_pratilipi, 'displayTitle', pratilipi['title'] if pratilipi['title'] != '' else pratilipi['title_en'])
            response_pratilipi = _set_key(response_pratilipi, 'authorId', pratilipi['author_id'])
            response_pratilipi = _set_key(response_pratilipi, 'readPageUrl', "/read?id=" + str(pratilipi['id']))
            response_pratilipi = _set_key(response_pratilipi, 'writePageUrl', "/pratilipi-write/?id=" + str(pratilipi['id']))

            pratilipi_slug = pratilipi['slug'] if pratilipi['slug'] != '' else pratilipi['slug_en']
            response_pratilipi = _set_key(response_pratilipi, 'slug', '/story/{}-{}'.format(pratilipi_slug, pratilipi['slug_id']))

            response_pratilipi = _set_key(response_pratilipi, 'type', pratilipi['type'])
            response_pratilipi = _set_key(response_pratilipi, 'contentType', pratilipi['content_type'])
            response_pratilipi = _set_key(response_pratilipi, 'summary', pratilipi['summary'] if pratilipi['summary'] is not None else "")
            response_pratilipi = _set_key(response_pratilipi, 'state', pratilipi['state'])
            response_pratilipi = _set_key(response_pratilipi, 'readingTime', pratilipi['reading_time'])
            response_pratilipi = _set_key(response_pratilipi, 'readCount', pratilipi['read_count'])
            response_pratilipi = _set_key(response_pratilipi, 'lastUpdatedDateMillis', int(pratilipi['updated_at'].strftime("%s")) * 1000)
            response_pratilipi = _set_key(response_pratilipi, 'listingDateMillis', int(pratilipi['created_at'].strftime("%s")) * 1000)
            response_pratilipi = _set_key(response_pratilipi, 'coverImageUrl', _pratilipi_cover_image(pratilipi['id'], pratilipi['cover_image']))
            response_pratilipi = _set_key(response_pratilipi, 'averageRating', "{0:.2f}".format(rating))

            data = {}
            data['authorId'] = author['id']
            data['displayName'] = _author_name(author)
            data['pageUrl'] = _author_slug_details(author)
            data['contentPublished'] = author['content_published']
            data['totalReadCount'] = author['total_read_count']
            data['profileImageUrl'] = supp_service.get_image_url(author['id'], author['profile_image'], 'image')
            data['slug'] = _author_slug_details(author)


            if feed['activity_type'] == 'RATED':
                response_object = _set_key(response_object, 'feedCreated',
                                           int(feed['activity_performed_at'].strftime("%s")) * 1000)
                response_object = _set_key(response_object, 'userRating', "{0:.2f}".format(int(feed['activity_value'])))
                response_object = _set_key(response_object, 'feedType', 'RATING')
            elif feed['activity_type'] == 'GENERIC':
                response_object = _set_key(response_object, 'feedCreated',
                                           int(pratilipi['published_at'].strftime("%s")) * 1000)
                response_object = _set_key(response_object, 'feedType', 'GENERIC')
                author_name = data['displayName']
                story_name = pratilipi['title'] if pratilipi['title'] != '' else pratilipi['title_en']
                message = translations.translations[kwargs['language']]['publish'].format(author_name = author_name, story_name = story_name)
                response_object = _set_key(response_object, 'feedMessage', message)
            else:
                response_object = _set_key(response_object, 'feedCreated',
                                           int(pratilipi['published_at'].strftime("%s")) * 1000)
                response_object = _set_key(response_object, 'feedType', 'PUBLISH')


            response_pratilipi = _set_key(response_pratilipi, 'author', data)
            response_object['pratilipi'] = response_pratilipi
            response_dict['feedList'].append(response_object)

    if kwargs['offset'] < 80 and len(feed_list) != 0:
        response_dict['finished'] = False
    else:
        response_dict['finished'] = True

    response_dict['offset'] = kwargs['offset']

    return response_dict

def for_top_authors(kwargs):
    """top authors"""
    response_dict = {'authorList': []}
    authors = kwargs['authors']
    logged_user_id = kwargs['logged_user_id']
    for author in authors:
        response = {}
        response = _set_key(response, 'authorId', author['author_id'])
        response = _set_key(response, 'firstName', author['first_name'])
        response = _set_key(response, 'name', author['first_name'])
        response = _set_key(response, 'averageRate', "{0:.2f}".format(author['average_rate']))
        response = _set_key(response, 'averageRatingCount', int(author['average_rating_count']))
        response = _set_key(response, 'totalReadCount', int(author['total_read']))
        response = _set_key(response, 'displayName', _author_name(author))
        response = _set_key(response, 'contentPublished', author['content_published'])
        response = _set_key(response, 'profileImageUrl', supp_service.get_image_url(author['author_id'], author['profile_image'], 'image'))
        response = _set_key(response, 'pageUrl', _author_slug_details(author))

        data = supp_service.follow_details([author['author_id']], [logged_user_id], logged_user_id)
        response = _set_key(response, 'following', data[author['author_id']]['following'] if data != {} else False)
        response = _set_key(response, 'followCount', data[author['author_id']]['followersCount'] if data != {} else 0)
        response_dict['authorList'].append(response)

    return json.dumps(response_dict)

def for_reader_score(kwargs):
    """reader score response"""
    response = {}
    response = _set_key(response, 'read_word_count', kwargs['read_word_count'])
    if kwargs['no_of_books_read'] is not None: response = _set_key(response, 'no_of_books_read', kwargs['no_of_books_read'])
    if kwargs['tier'] is not None: response = _set_key(response, 'tier', kwargs['tier'])
    return json.dumps(response)

def for_reader_dashboard(kwargs):
    """reader dasboard"""
    response = {}
    response = _set_key(response, 'word_count', int(kwargs['word_count']))
    response = _set_key(response, 'only_reviews', int(kwargs['only_reviews']))
    response = _set_key(response, 'rate_and_review', int(kwargs['rate_and_review']))
    response = _set_key(response, 'following_count', int(kwargs['following_count']))
    response = _set_key(response, 'read_categories', kwargs['read_categories'])
    return json.dumps(response)
