# db
class DbConnectionError(Exception):
    def __init__(self, err):
        self.message = 'db connection issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

class DbInsertError(Exception):
    def __init__(self, err):
        self.message = 'db insertion issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

class DbSelectError(Exception):
    def __init__(self, err):
        self.message = 'db select issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

class DbUpdateError(Exception):
    def __init__(self, err):
        self.message = 'db update issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

class RedisConnectionError(Exception):
    def __init__(self, err):
        self.message = 'redis connection issue; {}'.format(err)
    def __str__(self):
        return str(self.message)

# service specific
class LanguageInvalid(Exception):
    def __init__(self):
        self.message = 'invalid language'
    def __str__(self):
        return str(self.message)

class PratilipiNotFound(Exception):
    def __init__(self):
        self.message = 'no pratilipis found'
    def __str__(self):
        return str(self.message)

class FeedNotFound(Exception):
    def __init__(self):
        self.message = 'no feed entries found'
    def __str__(self):
        return str(self.message)

class LanguageRequired(Exception):
    def __init__(self):
        self.message = 'language is mandatory'
    def __str__(self):
        return str(self.message)

class FromSecRequired(Exception):
    def __init__(self):
        self.message = 'from sec is mandatory'
    def __str__(self):
        return str(self.message)

class ToSecRequired(Exception):
    def __init__(self):
        self.message = 'to sec is mandatory'
    def __str__(self):
        return str(self.message)

class AuthorIdRequired(Exception):
    def __init__(self):
        self.message = 'author id is mandatory'
    def __str__(self):
        return str(self.message)

class UserIdRequired(Exception):
    def __init__(self):
        self.message = 'user id is mandatory'
    def __str__(self):
        return str(self.message)

class NoDataFound(Exception):
    def __init__(self, err):
        self.message = 'no data found; {}'.format(err)
    def __str__(self):
        return str(self.message)

class PeriodInvalid(Exception):
    def __init__(self, err):
        self.message = 'invalid period in request'
    def __str__(self):
        return str(self.message)

class CategoryNotFound(Exception):
    def __init__(self):
        self.message = 'category not found'
    def __str__(self):
        return str(self.message)

