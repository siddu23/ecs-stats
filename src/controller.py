import bottle
import cognition
import response_builder
import inspect
import sys

from bottle import response, hook
from commonfns import request_parser, log, timeit, transform_request
from exceptions import *
from validator import *
from pprint import pprint as p
from conf import author_recommend_one
from conf import author_recommend_two
from conf import author_recommend_three

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

@timeit
@request_parser
def get_recent_published(**kwargs):
    """get recent published pratilipi"""
    try:
        # query param
        kwargs = transform_request(kwargs)

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
        """
        if kwargs['user_id'] > 0:
            librarys = cognition.get_libray_added(kwargs['user_id'], pratilipi_ids)
            library_dict = _object_to_dict(librarys)
        """

        response_kwargs = { 'pratilipis': pratilipis,
                            'authors': author_dict,
                            'ratings': rating_dict,
                            'librarys': library_dict,
                            'total_pratilipis': total_pratilipis,
                            'limit': kwargs['limit'],
                            'offset': kwargs['offset'] }

        response = response_builder.for_all(response_kwargs)

        sys.stdout.flush()
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

@timeit
@request_parser
def get_read_time(**kwargs):
    """get read time wise pratilipi"""
    try:
        # query param
        kwargs = transform_request(kwargs)

        # validate request
        validate_read_time_request(kwargs)

        # get pratilipis
        pratilipis, total_pratilipis = cognition.get_read_time(kwargs)

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
        """
        if kwargs['user_id'] > 0:
            librarys = cognition.get_libray_added(kwargs['user_id'], pratilipi_ids)
            library_dict = _object_to_dict(librarys)
        """

        response_kwargs = { 'pratilipis': pratilipis,
                            'authors': author_dict,
                            'ratings': rating_dict,
                            'librarys': library_dict,
                            'total_pratilipis': total_pratilipis,
                            'limit': kwargs['limit'],
                            'offset': kwargs['offset'] }

        response = response_builder.for_all(response_kwargs)

        sys.stdout.flush()
        return bottle.HTTPResponse(status=200, body=response)
    except LanguageRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except LanguageInvalid as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except FromSecRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except ToSecRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except PratilipiNotFound as err:
        return bottle.HTTPResponse(status=404)
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), kwargs)
        return bottle.HTTPResponse(status=500, body={"message": str(err)})

@timeit
@request_parser
def get_high_rated(**kwargs):
    """get high rated pratilipi"""
    try:
        # query param
        kwargs = transform_request(kwargs)

        # validate request
        validate_request(kwargs)

        # get pratilipis
        pratilipis, total_pratilipis, rating_dict = cognition.get_high_rated(kwargs)

        # get authors related to pratilipis
        author_ids = _join_authorids(pratilipis)
        authors = cognition.get_authors(author_ids)
        author_dict = _object_to_dict(authors)

        # get library related to pratilipis
        library_dict = {}
        """
        if kwargs['user_id'] > 0:
            librarys = cognition.get_libray_added(kwargs['user_id'], pratilipi_ids)
            library_dict = _object_to_dict(librarys)
        """

        response_kwargs = { 'pratilipis': pratilipis,
                            'authors': author_dict,
                            'ratings': rating_dict,
                            'librarys': library_dict,
                            'total_pratilipis': total_pratilipis,
                            'limit': kwargs['limit'],
                            'offset': kwargs['offset'] }

        response = response_builder.for_all(response_kwargs)

        sys.stdout.flush()
        return bottle.HTTPResponse(status=200, body=response)
    except LanguageRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except LanguageInvalid as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except FromSecRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except ToSecRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except PratilipiNotFound as err:
        return bottle.HTTPResponse(status=404)
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), kwargs)
        return bottle.HTTPResponse(status=500, body={"message": str(err)})

@timeit
@request_parser
def get_author_dashboard(**kwargs):
    """get author dashboard"""
    try:
        # query param
        kwargs['author_id'] = int(kwargs['authorid'][0]) if 'authorid' in kwargs else None
        kwargs['user_id'] = int(kwargs['logged_user_id']) if 'logged_user_id' in kwargs else 0

        validate_author_dashboard_request(kwargs)
        all_data = cognition.get_author_dashboard(kwargs)
        response = response_builder.for_author_dashboard(all_data)

        sys.stdout.flush()
        return bottle.HTTPResponse(status=200, body=response)
    except AuthorIdRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), kwargs)
        return bottle.HTTPResponse(status=500, body={"message": str(err)})

@timeit
@request_parser
def get_author_recommendations(**kwargs):
    """ Recommend authors """
    try:
        # query param
        language = kwargs['language'][0].lower() if 'language' in kwargs else None
        offset = kwargs['cursor'][0] if 'cursor' in kwargs else 0
        #bucket  = int(kwargs['bucket'][0]) if 'bucket' in kwargs else 1
        user_id = int(kwargs['logged_user_id']) if 'logged_user_id' in kwargs else 0
        authors = []
        author_ids = None
        limit = 20
        bucket = 'A1' 
        temp = user_id % 10

        if offset == None or offset == "null":
            offset = 0
        else:
            offset = int(offset) 
        
        if temp <= 3:
            bucket = 'A1'
        elif temp <= 6:
            bucket = 'A2'
        elif temp <=9:
            bucket = 'A3'

        #print language, offset, bucket, user_id, limit

        if(bucket == 'A1'):
            author_ids = author_recommend_one
        elif(bucket == 'A2'):
            author_ids = author_recommend_two
        elif(bucket == 'A3'):
            author_ids = author_recommend_three
   
        if language == "hindi":
            ids = author_ids.hindi_authors
        elif language == "bengali":
            ids = author_ids.bengali_authors
        elif language == "gujarati":
            ids = author_ids.gujarati_authors
        elif language == "kannada":
            ids = author_ids.kannada_authors
        elif language == "malayalam":
            ids = author_ids.malayalam_authors
        elif language == "marathi":
            ids = author_ids.marathi_authors
        elif language == "tamil":
            ids = author_ids.tamil_authors
        elif language == "telugu":
            ids = author_ids.telugu_authors
        else:
            return bottle.HTTPResponse(status=400, body={"message": "Language is required"})

        user_followed_authors = cognition.get_user_followed_authorIds(user_id)
        #print user_followed_authors

        authors = []
        for _id in user_followed_authors:
            if _id in ids:
                ids.remove(_id)
            
        ids = ids[offset:(offset+limit)]
        idStr = ','.join(map(str, ids))
            #print "Getting authors for ", idStr 
        if(len(idStr) > 0):
            authors = cognition.get_authors(idStr)
            #print authors

        response_kwargs = {'authors':authors,
                            'cursor':offset,
                            'logged_user_id':user_id,
                            'bucket':bucket}

        response = response_builder.for_author_recommendations(response_kwargs)
 
        sys.stdout.flush()
        return bottle.HTTPResponse(status=200, body=response)
        
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), kwargs)
        return bottle.HTTPResponse(status=500, body={"message": str(err)})


@timeit
@request_parser
def get_user_feed(**kwargs):
    """ get user feed """
    try:
        print(kwargs)
        validate_user_feed_request(kwargs)
        offset = int(kwargs['offset'][0]) if kwargs.has_key('offset') else 0
        feed_pratilipi_list, offset = cognition.get_user_feed(kwargs['logged_user_id'], offset)

        # get authors related to pratilipis
        author_ids = _join_authorids(feed_pratilipi_list)
        authors = cognition.get_authors(author_ids)
        author_dict = _object_to_dict(authors)

        # get ratings related to pratilipis
        pratilipi_ids = _join_pratilipiids(feed_pratilipi_list)
        ratings = cognition.get_ratings(pratilipi_ids)
        rating_dict = _object_to_dict(ratings)

        response_kwargs = {'pratilipis': feed_pratilipi_list,
                           'authors': author_dict,
                           'ratings': rating_dict,
                           'offset': offset}

        response = response_builder.for_user_feed(response_kwargs)
        sys.stdout.flush()
        return bottle.HTTPResponse(status=200, body=response)
    except UserIdRequired as err:
        return bottle.HTTPResponse(status=400, body={"message": str(err)})
    except FeedNotFound as err:
        return bottle.HTTPResponse(status=404, body={"message": str(err)})
    except Exception as err:
        print(str(err))
        return bottle.HTTPResponse(status=500, body={"message": str(err)})