#!/bin/bash 
set -e 
echo "starting nginx ......"
exec service nginx start &
echo "starting gunicorn ......"
exec gunicorn -c gunicorn_conf.py wsgi
echo "service startup done"
