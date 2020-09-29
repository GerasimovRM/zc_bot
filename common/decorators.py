from time import sleep


def after_sleep(time_sleep=0.1):
    def inner(func):
        def wrapper(*args, **kwargs):
            sleep(time_sleep)
            result = func(*args, **kwargs)
            return result
        return wrapper
    return inner
