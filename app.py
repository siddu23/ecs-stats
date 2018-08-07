import sys
import router

from bottle import Bottle, error

# setting encoding for app
reload(sys)
sys.setdefaultencoding('utf-8')

# define application
application = Bottle()

@application.error(500)
def custom500(error):
    return 'ERROR - service internal error'

# load app routes
router.app_routes(application)

print "worker ready to accept requests...."
