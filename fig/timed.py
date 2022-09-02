def timed(fn):
    from time import perf_counter
    from functools import wraps
    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        elapsed = end -start
        print('{} took {:.6f}s  to run'.format(fn.__name__, elapsed))
        return result
    return inner