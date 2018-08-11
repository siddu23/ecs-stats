import os
import requests
import ujson
import inspect

from conf import config
from commonfns import timeit, log

AUTH_SERVICE = config.AUTH_SERVICE_URL
FOLLOW_SERVICE = config.FOLLOW_SERVICE_URL

REQUEST_TIMEOUT = config.SLOW_RUNNING_CALLS
STAGE = config.STAGE

#====================================
#auth service integrations
#====================================
@timeit
def has_access_to_update(user_id, author_id):
    """has access to update author details"""
    try:
        if int(user_id) == 0: return False
        url = '{}/auth/isAuthorized'.format(AUTH_SERVICE)
        headers = {'User-Id': str(user_id), 'Service-Id': 'AUTHOR'}
        param_dict = {'resource': '%2Fauthors', 'method': 'PATCH', 'id': author_id}
        r = requests.get(url, params=param_dict, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200: return False
        data = ujson.loads(r.text)
        return data['data'][0]['isAuthorized']
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), {'user_id': user_id, 'author_id': author_id})
        return False

#====================================
#follow service integrations
#====================================
@timeit
def follow_details(author_ids, user_ids, logged_user_id):
    """follow details"""
    try:
        author_ids = ','.join(str(i) for i in author_ids)
        user_ids = ','.join(str(i) for i in user_ids)

        url = '{}/follows/v2.0/meta_data'.format(FOLLOW_SERVICE) 
        headers = {'User-Id': str(logged_user_id), 'Service-Id': 'AUTHOR'}
        param_dict = {'referenceType': 'AUTHOR', 'referenceId': author_ids, 'userId': user_ids}
        r = requests.get(url, params=param_dict, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code != 200: return {}

        temp = ujson.loads(r.text)
        data = dict((int(i), temp[i]) for i in temp)
        return data
    except Exception as err:
        log(inspect.stack()[0][3], "ERROR", str(err), {'author_ids': author_ids, 'user_ids': user_ids, 'logged_user_id': logged_user_id})
        return {}

#====================================
#image service
#====================================
def get_image_url(author_id, image, img_type):
    """image url"""
    author_id = int(author_id)
    sub_domain_number = author_id % 5 if image is not None else 0
    prefix = '/api' if STAGE == 'devo' else 'https://{}.ptlp.co'.format(sub_domain_number)
    suffix = '/author/{}?authorId={}&version={}'.format(img_type, author_id, image) if image is not None else '/author/{}'.format(img_type)
    return "{}{}".format(prefix,suffix)
