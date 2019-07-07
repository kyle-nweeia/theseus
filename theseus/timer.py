from functools import wraps
from time import perf_counter

def timer(function):
    @wraps(function)
    def wrapper(*args):
        start = perf_counter()
        value = function(*args)
        print(f'{function.__name__}: {perf_counter() - start} seconds')
        return value
    wrapper.unwrapped = function
    return wrapper