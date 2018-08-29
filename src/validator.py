from exceptions import *
from conf.config import LANGUAGE


def validate_request(req):
    if req['language'] is None:
        raise LanguageRequired

    if req['category'] is None:
        raise PratilipiNotFound

    if req['language'].lower() not in LANGUAGE:
        raise LanguageInvalid

def validate_read_time_request(req):
    if req['language'] is None:
        raise LanguageRequired

    if req['category'] is None:
        raise PratilipiNotFound

    if req['language'].lower() not in LANGUAGE:
        raise LanguageInvalid

def validate_author_dashboard_request(req):
    if req['author_id'] is None:
        raise AuthorIdRequired

def validate_user_feed_request(req):
    if req['logged_user_id'] is None:
        raise UserIdRequired
    elif not req['logged_user_id'] > 0:
        raise UserIdRequired

def validate_reader_score_request(req):
    if req['user_id'] is None:
        raise UserIdRequired

def validate_top_authors_request(req):
    if req['language'] is None:
        raise LanguageRequired

    if req['language'].lower() not in LANGUAGE:
        raise LanguageInvalid

def validate_continue_reading_request(req):
    if req['user_id'] is None or req['user_id'] == 0:
        raise UserIdRequired
