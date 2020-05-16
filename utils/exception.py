from functools import wraps
from utils.logger import log_error
import sys, traceback

class ValidationError(Exception):
    """The exception will be raised when a validation failed in models"""

    def __init__(self, message):
        super().__init__(message)

def excpetion_handler(fn):
    """The decorator handles exceptions within the framework.

    A message will be returned to the user when a ValidationError was raised.
    Otherwise, a message indicating an internal error will be given. And the
    error will be logged by the logger.

    If the function returns None, a dict {'status': 200} will be returned.
    Otherwise, the returned value of the wrapped function will be returned.
    """
    def handler(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            if res is not None:
                return res
        except ValidationError as e:
            return {'error': str(e)}
        except Exception as e:
            log_error(str(e))
            traceback.print_exc(file=sys.stdout)
            return {'error': 'Internal error.'}
        return {'status': 200}
    return handler
