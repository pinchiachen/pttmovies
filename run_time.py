import time
import datetime


def calculate_run_time(func):
    def wrapper(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        times = time.time() - start_time
        print(f'Execution Time: {datetime.timedelta(seconds=times)}')
    return wrapper