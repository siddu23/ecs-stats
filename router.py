from src import controller

def app_routes(app):
    # health calls
    app.route('/health', ['OPTIONS', 'GET'], controller.health)

    # ping db
    app.route('/pingdb', ['OPTIONS', 'GET'], controller.pingdb)

    # /stats/v1.0/recent_published?language=HINDI&category=romance&limit=10&offset=0
    app.route('/stats/v1.0/recent_published', ['GET', 'OPTIONS'], controller.get_recent_published)

    # /stats/v1.0/high_rated?language=HINDI&category=romance&limit=10&offset=0
    app.route('/stats/v1.0/high_rated', ['GET', 'OPTIONS'], controller.get_high_rated)

    # /stats/v1.0/read_time?language=HINDI&category=romance&fromSec=0&toSec=120&limit=10&offset=0
    app.route('/stats/v1.0/read_time', ['GET', 'OPTIONS'], controller.get_read_time)

