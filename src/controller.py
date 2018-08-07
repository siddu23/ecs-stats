import bottle
import cognition
import response_builder
import inspect

from bottle import response, hook
from commonfns import request_parser, log
from exceptions import *
from validator import *
from pprint import pprint as p

@hook('after_request')
def set_content_type():
    """set response content type"""
    response.set_header('Content-Type', 'application/json; charset=utf-8')
    response.set_header('Powered-By', 'Bottle 0.12.13')

def health():
    """health check"""
    return bottle.HTTPResponse(status=200, body=cognition.health())

@request_parser
def pingdb(**kwargs):
    """ping db"""
    try:
        data = cognition.ping_db(kwargs)
        response = response_builder.for_ping(data)
        return bottle.HTTPResponse(status=200, body=response)
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), kwargs)
        return bottle.HTTPResponse(status=500, body={"message": str(err)})

def _join_authorids(pratilipis):
    author_list = []
    for i in pratilipis:
        author_list.append(i.author_id.__str__())
    return ','.join(author_list)

def _join_pratilipiids(pratilipis):
    pratilipi_list = []
    for i in pratilipis:
        pratilipi_list.append(i.id.__str__())
    return ','.join(pratilipi_list)

def _object_to_dict(obj):
    obj_dict = {}
    for i in obj:
        obj_dict[i.id] = i.__dict__
    return obj_dict

@request_parser
def get_recent_published(**kwargs):
    """get recent published pratilipi"""
    try:
        # query param
        kwargs['language'] = kwargs['language'][0] if 'language' in kwargs else None
        kwargs['category'] = kwargs['category'][0] if 'category' in kwargs else None
        kwargs['user_id'] = int(kwargs['logged_user_id']) if 'logged_user_id' in kwargs else 0
        kwargs['limit'] = int(kwargs['limit'][0]) if 'limit' in kwargs else 20
        kwargs['offset'] = int(kwargs['offset'][0]) if 'offset' in kwargs else 0

        # validate request
        validate_request(kwargs)

        # get pratilipis
        pratilipis, total_pratilipis = cognition.get_recent_published(kwargs)

        # get authors related to pratilipis
        author_ids = _join_authorids(pratilipis)
        authors = cognition.get_authors(author_ids)
        author_dict = _object_to_dict(authors)

        # get ratings related to pratilipis
        pratilipi_ids = _join_pratilipiids(pratilipis)
        ratings = cognition.get_ratings(pratilipi_ids)
        rating_dict = _object_to_dict(ratings)

        # get library related to pratilipis
        library_dict = {}
        if kwargs['user_id'] > 0:
            librarys = cognition.get_libray_added(kwargs['user_id'], pratilipi_ids)
            library_dict = _object_to_dict(librarys)

        response_kwargs = { 'pratilipis': pratilipis,
                            'authors': author_dict,
                            'ratings': rating_dict,
                            'librarys': library_dict,
                            'total_pratilipis': total_pratilipis,
                            'limit': kwargs['limit'],
                            'offset': kwargs['offset'] }

        response = response_builder.for_all(response_kwargs)

        return bottle.HTTPResponse(status=200, body=response)
    except LanguageRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except LanguageInvalid as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except PratilipiNotFound as err:
        return bottle.HTTPResponse(status=404)
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), kwargs)
        return bottle.HTTPResponse(status=500, body={"message": str(err)})

