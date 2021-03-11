import logging
import os
import sys
import time
from functools import wraps
from typing import Optional

logger = logging.getLogger(__name__)


def is_debug_active() -> bool:
    # https://stackoverflow.com/questions/38634988/check-if-program-runs-in-debug-mode
    gettrace = getattr(sys, "gettrace", None)
    if gettrace is not None and gettrace():
        return True
    return False


def get_environment_variable(key: str, default_value: str = None) -> Optional[str]:
    value = None
    try:
        value = os.environ[key]
    except KeyError:
        if default_value is not None:
            value = default_value
        pass
    return value


def timer(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        logging.info(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value

    return wrapper_timer
