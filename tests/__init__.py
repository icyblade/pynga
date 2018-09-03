import os


def local(func):
    def wrapper(*args, **kwargs):
        if 'TRAVIS' not in os.environ:
            func(*args, **kwargs)

    return wrapper
