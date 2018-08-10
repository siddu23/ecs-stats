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

<<<<<<< HEAD
    # /stats/v1.0/author_dashboard?authorId=2
    app.route('/stats/v1.0/author_dashboard', ['GET', 'OPTIONS'], controller.get_author_dashboard)

=======
    # /authors/recommendation 
    app.route('/authors/recommendation', ['GET'], controller.get_author_recommendations)
>>>>>>> 9383e30d5869059892b6ba26b5d4ff9f0dd4db14
