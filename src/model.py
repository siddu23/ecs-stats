from datetime import datetime


PRATILIPI_INT_ATTR = ['id', 'author_id', 'page_count', 'read_count', 'reading_time', 'event_id']
PRATILIPI_STR_ATTR = ['content_type', 'language', 'type', 'cover_image', 'title', 'title_en', 'slug', 'slug_en', 'slug_id']

AUTHOR_INT_ATTR = ['id']
AUTHOR_STR_ATTR = ['first_name', 'first_name_en', 'last_name', 'last_name_en', 'pen_name', 'pen_name_en', 'firstname_lastname', 'firstname_lastname_en', 'slug']

RATING_INT_ATTR = ['id', 'avg_rating']

LIBRARY_STR_ATTR = ['id', 'state']

PING_INT_ATTR = []
PING_STR_ATTR = []
PING_DT_ATTR = ['dt']

class PingDB:
    def __init__(self, kwargs=[], full=True):
        """init"""
        setattr(self, 'name', 'pingdb')
        if full:
            for name in PING_STR_ATTR: setattr(self, name, None)
            for name in PING_INT_ATTR: setattr(self, name, 0)
            for name in PING_DT_ATTR: setattr(self, name, datetime.utcnow())
        for name in kwargs:
            setattr(self, name, kwargs[name])

class Pratilipi:
    def __init__(self, kwargs=[], full=True):
        """init"""
        setattr(self, 'name', 'pratilipi')
        if full:
            for name in PRATILIPI_STR_ATTR: setattr(self, name, None)
            for name in PRATILIPI_INT_ATTR: setattr(self, name, 0)
        for name in kwargs:
            setattr(self, name, kwargs[name])

class Author:
    def __init__(self, kwargs=[], full=True):
        """init"""
        setattr(self, 'name', 'author')
        if full:
            for name in AUTHOR_STR_ATTR: setattr(self, name, None)
            for name in AUTHOR_INT_ATTR: setattr(self, name, 0)
        for name in kwargs:
            setattr(self, name, kwargs[name])

class Rating:
    def __init__(self, kwargs=[], full=True):
        """init"""
        setattr(self, 'name', 'rating')
        if full:
            for name in RATING_INT_ATTR: setattr(self, name, 0)
        for name in kwargs:
            setattr(self, name, kwargs[name])

class Library:
    def __init__(self, kwargs=[], full=True):
        """init"""
        setattr(self, 'name', 'library')
        if full:
            for name in LIBRARY_STR_ATTR: setattr(self, name, 0)
        for name in kwargs:
            setattr(self, name, kwargs[name])
