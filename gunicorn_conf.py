import os
import sys
import pymysql.cursors

from os import environ, path
sys.path.append( path.dirname( path.abspath(__file__) ) )
import __builtin__
from conf.config import DB_REPLICA
from conf.category_map import CATEGORY_MAP

from gevent import monkey
monkey.patch_all(thread=False, socket=False)

#gunicorn worker details
worker_class = 'gevent'
workers = 2

#per worker config
worker_connections = 4096
backlog = 2048

#session config
keep_alive = 5
timeout = 60

#wsgi socket details
bind = 'unix:service.sock'

#owner details
user = os.environ['USER'] if os.environ['STAGE'] in ('local') else 'root'
group = os.environ['USER'] if os.environ['STAGE'] in ('local') else 'www-data'
umask = '007'

#logging
accesslog = None
errorlog = '-'
syslog = True

def post_fork(server, worker):
    # Connect to the database
    connection = pymysql.connect(host=DB_REPLICA['host'],
                                 user=DB_REPLICA['user'],
                                 password=DB_REPLICA['pass'],
                                 db='author',
                                 autocommit=True,
                                 connect_timeout=86400,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    __builtin__.CONN_RO = connection

    data = {}
    for category in CATEGORY_MAP:
        for content_type in CATEGORY_MAP[category]:
            for lang in CATEGORY_MAP[category][content_type]:
                end_point = CATEGORY_MAP[category][content_type][lang]
                k = "{}|{}".format(lang.upper(), end_point.lower())
                data[k] = (content_type.upper(), category.lower())
    __builtin__.CATEGORY_MAP = data

    print "gunicorn worker conneted to db"

def worker_exit(server, worker):
    __builtin__.CONN_RO.close()
    print "gunicorn worker db connection closed"
