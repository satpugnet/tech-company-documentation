import logging
import time
from logging.config import dictConfig

import colors
from flask import request, g


class CustomFormatter(logging.Formatter):
    """
    Logging Formatter to add colors
    """

    BASE_FORMAT = "[%(asctime)s] {} [%(module)s]: %(message)s"
    MAX_SPACE = 10

    FORMATS = {
        logging.DEBUG: BASE_FORMAT.format(
            colors.color("DEBUG".center(MAX_SPACE), 'black', bg='grey')
        ),
        logging.INFO: BASE_FORMAT.format(
            colors.color("INFO".center(MAX_SPACE), 'black', bg='cyan')
        ),
        logging.WARNING: BASE_FORMAT.format(
            colors.color("WARNING".center(MAX_SPACE), 'black', bg='yellow')
        ),
        logging.ERROR: BASE_FORMAT.format(
            colors.color("ERROR".center(MAX_SPACE), 'black', bg='red')
        ),
        logging.CRITICAL: BASE_FORMAT.format(
            colors.color("CRITICAL".center(MAX_SPACE), 'black', bg='red')
        )
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            '()': CustomFormatter,
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

LOGGER = logging.getLogger()


def get_logger():
    return LOGGER


def init(app):
    """
    Initialise the logging
    """

    # Http logging improved
    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        now = time.time()
        duration_in_s = round(now - g.start, 3)

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host
        args = dict(request.args)

        log_params = [
            ('host', host, 'red'),
            ('ip', ip, 'red'),
            ('method', request.method, 'blue'),
            ('path', request.path, 'blue'),
            ('params', args, 'blue'),
            ('status', response.status_code, 'yellow'),
            ('duration', '{}s'.format(duration_in_s), 'green'),
        ]

        line = " ".join([colors.color("{}={}".format(name, value), fg=color) for name, value, color in log_params])
        get_logger().info(line)

        return response
