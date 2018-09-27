import __builtin__

from exceptions import *
from conf.config import LANGUAGE, AVAILABLE_PERIODS

category_map = __builtin__.CATEGORY_MAP

def validate_request(req):
    if req['language'] is None:
        raise LanguageRequired

    if req['category'] is None:
        raise PratilipiNotFound

    if req['language'].lower() not in LANGUAGE:
        raise LanguageInvalid

    if req['content_type'] is None or req['internal_category_name'] is None:
        raise CategoryNotFound

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

    if req['period'] not in AVAILABLE_PERIODS and req['period'] != None:
        raise PeriodInvalid

def validate_continue_reading_request(req):
    if req['user_id'] is None or req['user_id'] == 0:
        raise UserIdRequired

    if req['language'] is None:
        raise LanguageRequired

    if req['language'].lower() not in LANGUAGE:
        raise LanguageInvalid

def validate_reader_dashboard_request(req):
    if req['user_id'] is None or req['user_id'] == 0:
        raise UserIdRequired

def validate_for_you_request(req):
    if req['user_id'] is None or req['user_id'] == 0:
        raise UserIdRequired
