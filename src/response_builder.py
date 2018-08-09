import json

from datetime import datetime
from commonfns import timeit
from pprint import pprint as p

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

def _pratilipi_cover_image(pratilipi):
    pratilipi_id = int(pratilipi.id)
    sub_domain_number = pratilipi_id % 5 if pratilipi.cover_image is not None else 0
    prefix = 'https://{}.ptlp.co'.format(sub_domain_number)
    suffix = '/pratilipi/cover?apratilipiId={}&version={}'.format(pratilipi_id, pratilipi.cover_image) if pratilipi.cover_image is not None else '/pratilipi/cover'
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

    response = _set_key(response, 'coverImageUrl', _pratilipi_cover_image(pratilipi))
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
