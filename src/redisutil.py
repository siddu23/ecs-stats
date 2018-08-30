import redis

from conf.config import REDIS

class _RedisConnectionError(Exception):
    def __init__(self, err):
        self.message = 'redis connection issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

def connect_redis():
    """Connects to redis instance"""
    try:

        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        redis_connection = redis.StrictRedis(host=REDIS['host'],
                              port=int(REDIS['port']),
                              db=int(REDIS['db']),
                              decode_responses=True)

        print 'REDIS CONNECTED'
        # step 4: Set the hello message in Redis

        print "connected to db"
    except Exception as err:
        raise _RedisConnectionError(err)
    return redis_connection

def disconnect_redis(connection):
    connection.connection_pool.disconnect()
    print 'REDIS DISCONNECTED'
