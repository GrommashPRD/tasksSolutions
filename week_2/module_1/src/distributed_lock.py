import time
import datetime
import redis
from functools import wraps

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def single(max_processing_time):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lock_key = f"lock:{func.__module__}:{func.__name__}"
            lock_acquired = r.set(
                lock_key,
                'locked',
                ex=int(max_processing_time.total_seconds()),
                nx=True
            )

            if not lock_acquired:
                print(f"Функция {func.__name__} уже выполняется.")
                return

            try:
                return func(*args, **kwargs)
            finally:
                r.delete(lock_key)

        return wrapper
    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    print("start")
    time.sleep(2)
    print("end")


if __name__ == "__main__":
    process_transaction()