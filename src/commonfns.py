import re
import os
import time

from datetime import datetime
from functools import wraps
from bottle import request
from conf import config

DEBUG_MODE = config.DEBUG_MODE
SLOW_RUNNING_CALLS = config.SLOW_RUNNING_CALLS

empty2none = lambda s: None if s is '' else s

def request_parser(function):
    """decorator for request parser"""

    @wraps(function)
    def parse_request(**kwargs):
        param_dict = {}
        if request.method in ("GET", "DELETE", "PATCH"):
            query_dict = request.query.__dict__
            param_dict = query_dict['dict']
        if request.method in ("POST", "PUT"):
            if request.headers.get('content-type') == 'application/json':
                param_dict = ujson.loads(request.body.read())
            else:
                k = request.forms.keys()
                v = request.forms.values()
                param_dict = dict(zip(k, v))

        param_dict = dict((k, empty2none(v)) for k, v in param_dict.iteritems())

        param_dict['logged_user_id'] = request.headers.get('User-Id', 0)
        param_dict['version'] = str(requested_api_version(request.headers))
        param_dict['access_token'] = request.headers.get('Access-Token', '')
        param_dict['service_id'] = request.headers.get('Service-Id', '')
        param_dict['request_id'] = request.headers.get('Request-Id', '')

        # convert all keys to lowercase
        param_dict = dict((k.lower(), v) for k, v in param_dict.iteritems())

        # merge all parameters
        kwargs = dict(kwargs.items() + param_dict.items())
        return function(**kwargs)
    return parse_request

def requested_api_version(data):
    accepttxt = data.get('Accept', "Version=1.0")
    searchtxt = re.search(r'version=(\d.\d)', accepttxt.lower())
    version = 1.0
    if searchtxt:
        version = searchtxt.group()[-3:]
    return version

def log(fname, level, msg, args):
    """
    if (not level == "ERROR") or (not DEBUG_MODE):
        return
    """
    var = "[%s] [%s] - %s%s%s" % (level, fname, msg, "\n", args)
    print var

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        tt = int((te - ts) * 1000)
        """
        if tt <= SLOW_RUNNING_CALLS:
            return result
        """
        ft = "timetaken - {0:4d} ms".format(tt)
        var = "[%s] [%s] [%s] - %s" % ("INFO", os.getpid(), method.__name__, ft)
        print var
        return result
    return timed

def transform_request(kwargs):
    kwargs['language'] = kwargs['language'][0] if 'language' in kwargs else None
    kwargs['category'] = kwargs['category'][0] if 'category' in kwargs else None
    kwargs['from_sec'] = int(kwargs['fromsec'][0]) if 'fromsec' in kwargs else 0
    kwargs['to_sec'] = int(kwargs['tosec'][0]) if 'tosec' in kwargs else 9999999
    kwargs['user_id'] = int(kwargs['logged_user_id']) if 'logged_user_id' in kwargs else 0
    kwargs['limit'] = int(kwargs['limit'][0]) if 'limit' in kwargs else 20
    kwargs['offset'] = int(kwargs['offset'][0]) if 'offset' in kwargs else 0
    return kwargs

def transform_request_top_authors(kwargs):
    kwargs['language'] = kwargs['language'][0] if 'language' in kwargs else None
    kwargs['period'] = kwargs['period'][0] if 'period' in kwargs else None
    kwargs['category'] = kwargs['category'][0] if 'category' in kwargs else None
    kwargs['from_sec'] = int(kwargs['fromsec'][0]) if 'fromsec' in kwargs else 0
    kwargs['to_sec'] = int(kwargs['tosec'][0]) if 'tosec' in kwargs else 9999999
    kwargs['user_id'] = int(kwargs['logged_user_id']) if 'logged_user_id' in kwargs else 0
    kwargs['limit'] = int(kwargs['limit'][0]) if 'limit' in kwargs else 20
    kwargs['offset'] = int(kwargs['offset'][0]) if 'offset' in kwargs else 0
    return kwargs

def transform_request_v1(kwargs):
    kwargs['user_id'] = int(kwargs['userid'][0]) if 'userid' in kwargs else 0
    kwargs['limit'] = int(kwargs['limit'][0]) if 'limit' in kwargs else 20
    kwargs['offset'] = int(kwargs['offset'][0]) if 'offset' in kwargs else 0
    return kwargs
