import logging
logger = logging.getLogger(__name__)

def log_calls(func):
    """ a decorator to log the calls and returns of specific functions for debugging purposes """
    def logged(*args, **kwargs):
        logger.debug("calling {0}({1}{2})".format(func.__name__, str(args), str(kwargs)))
        result = func(*args, **kwargs)
        logger.debug("{0} returned {1}".format(func.__name__, str(result)))
        return result
    return logged

def print_calls(func):
    """ a decorator to print the calls and returns of specific functions for debugging purposes """
    def logged(*args, **kwargs):
        print("calling {0}({1}{2})".format(func.__name__, str(args), str(kwargs)))
        result = func(*args, **kwargs)
        print("{0} returned {1}".format(func.__name__, str(result)))
        return result
    return logged

def boardify(size, input):
    """ format a string representation of a board by putting in newlines at appropriate places """
    return '\n'.join([input[2*size*i:(2*size*(i+1))] for i in range(size)])
