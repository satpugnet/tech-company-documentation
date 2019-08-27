from functools import wraps

from github import TwoFactorException, BadAttributeException, RateLimitExceededException, BadUserAgentException, \
    UnknownObjectException, BadCredentialsException

from tools import logger


class GithubExceptionHandler:
    """
    Handle github exceptions for all call to github.
    """

    @staticmethod
    def github_exception_handler(f):

        @wraps(f)
        def wrap(*args, **kwargs):

            try:
                return f(*args, **kwargs)

            except BadCredentialsException as e:
                logger.get_logger().error("Github facade, invalid credentials \n%s", e)

            except UnknownObjectException as e:
                logger.get_logger().error("Github facade, unknown object \n%s", e)

            except BadUserAgentException as e:
                logger.get_logger().error("Github facade, bad user agent \n%s", e)

            except RateLimitExceededException as e:
                logger.get_logger().error("Github facade, rate limit exceeded \n%s", e)

            except BadAttributeException as e:
                logger.get_logger().error("Github facade, bad attribute \n%s", e)

            except TwoFactorException as e:
                logger.get_logger().error("Github facade, two factor error \n%s", e)

            except Exception as e:
                logger.get_logger().error("Github facade, unknown exception thrown \n%s", e)

        return wrap
