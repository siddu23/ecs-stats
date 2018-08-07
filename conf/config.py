import os

STAGE = os.environ.get("STAGE", "local").lower()

DB = {'name': 'pratilipi', 
      'host': os.environ.get('MASTER_DB_ENDPOINT_RW'),
      'port': os.environ.get('MASTER_DB_PORT'),
      'user': os.environ.get('MASTER_MYSQL_DB_USERNAME'),
      'pass': os.environ.get('MASTER_MYSQL_DB_PASSWORD')}

# application logging on/off switch
DEBUG_MODE = False if STAGE == 'prod' else True
SLOW_RUNNING_CALLS = 50 # in ms

LANGUAGE = ['hindi', 'marathi', 'tamil', 'telugu', 'bengali', 'kannada', 'gujarati', 'malayalam']

