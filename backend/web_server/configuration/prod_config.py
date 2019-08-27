from web_server.configuration.base_config import BaseConfig


class ProdConfig(BaseConfig):
    """
    Prod specific configuration for the flask app.
    """

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
