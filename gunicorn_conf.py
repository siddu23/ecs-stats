import os
import sys
import pymysql.cursors

from os import environ, path
sys.path.append( path.dirname( path.abspath(__file__) ) )

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
user = os.environ['USER'] if os.environ['STAGE'] in ('local', 'devo') else 'root'
group = os.environ['USER'] if os.environ['STAGE'] in ('local', 'devo') else 'www-data'
umask = '007'

#logging
accesslog = None
errorlog = '-'
syslog = True
