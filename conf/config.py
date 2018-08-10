import os

STAGE = os.environ.get("STAGE", "local").lower()
API_END_POINT = 'http://localhost' if 'API_END_POINT' not in os.environ else os.environ['API_END_POINT']
DB = {'name': 'pratilipi', 
      'host': os.environ.get('MASTER_DB_ENDPOINT_RW'),
      'port': os.environ.get('MASTER_DB_PORT'),
      'user': os.environ.get('MASTER_MYSQL_DB_USERNAME'),
      'pass': os.environ.get('MASTER_MYSQL_DB_PASSWORD')}

# application logging on/off switch
DEBUG_MODE = False if STAGE == 'prod' else True
SLOW_RUNNING_CALLS = 50 # in ms

LANGUAGE = ['hindi', 'marathi', 'tamil', 'telugu', 'bengali', 'kannada', 'gujarati', 'malayalam']

# 3rd party services details
AUTH_SERVICE_URL = API_END_POINT
FOLLOW_SERVICE_URL = API_END_POINT
