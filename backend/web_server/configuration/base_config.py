import datetime


class BaseConfig(object):
    """
    Base configuration for the flask app.
    """
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
