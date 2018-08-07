import pymysql.cursors

from conf.config import DB

class _DbConnectionError(Exception):
    def __init__(self, err):
        self.message = 'db connection issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

def connectdb():
    # Connect to the database
    try:
        connection = pymysql.connect(host=DB['host'],
                                     user=DB['user'],
                                     password=DB['pass'],
                                     db=DB['name'],
                                     port=int(DB['port']),
                                     autocommit=True,
                                     connect_timeout=86400,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        print "connected to db"
    except Exception as err:
        raise _DbConnectionError(err)
    return connection

def disconnectdb(conn):
    conn.close()
    print "disconnected to db"

