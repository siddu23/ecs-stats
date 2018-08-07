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

    if req['from_sec'] is None:
        raise FromSecRequired

    if req['to_sec'] is None:
        raise ToSecRequired
