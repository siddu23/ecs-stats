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

    # /stats/v1.0/author_dashboard?authorId=2
    app.route('/stats/v1.0/author_dashboard', ['GET', 'OPTIONS'], controller.get_author_dashboard)

    # /stats/v1.0/reader_dashboard?userid=2
    app.route('/stats/v1.0/reader_dashboard', ['GET', 'OPTIONS'], controller.get_reader_dashboard)

    # /stats/v1.0/top_authors
    app.route('/stats/v1.0/top_authors', ['GET', 'OPTIONS'], controller.get_top_authors)

    # /authors/recommendation
    app.route('/authors/recommendation', ['GET'], controller.get_author_recommendations)

    # /stats/v1.0/feed?offset=1234567
    app.route('/stats/v1.0/feed', ['GET'], controller.get_user_feed)

    # /stats/v1.0/most_active?offset=1234567
    app.route('/stats/v1.0/most_active', ['GET'], controller.get_most_active_authors)

    # /stats/v1.0/reader_score?userid=12345
    app.route('/stats/v1.0/reader_score', ['GET', 'OPTIONS'], controller.get_reader_score)

    # /stats/v1.0/continue_reading?userid=12345
    app.route('/stats/v1.0/continue_reading', ['GET', 'OPTIONS'], controller.get_continue_reading)

    # /stats/v1.0/for_you?userid=12345
    app.route('/stats/v1.0/for_you', ['GET'], controller.get_for_you)
