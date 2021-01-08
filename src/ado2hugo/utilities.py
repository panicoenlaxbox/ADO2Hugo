import sys
import os


def is_debug_active():
    # https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is not None and gettrace():
        return True
    return False


def get_environment_variable(key):
    value = None
    try:
        value = os.environ[key]
    except KeyError:
        pass
    return value
