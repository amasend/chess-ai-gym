import time
from functools import wraps


def timeit(f):
    """Decorator to measure running time of the method."""
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        value = f(*args, **kwargs)
        print(f"Running time \"{f.__name__}\": {time.time() - start_time}")
        return value
    return wrapper
