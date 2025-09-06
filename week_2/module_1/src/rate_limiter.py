import random
import time
import redis
from typing import Optional


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(
            self,
            redis_host: str = 'localhost',
            redis_port: int = 6379,
            max_requests: int = 5,
            time_window: int = 3
    ):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.max_requests = max_requests
        self.time_window = time_window
        self.key_prefix = "rate_limit:"

    def test(self) -> bool:
        current_time = int(time.time())
        key = f"{self.key_prefix}{current_time}"

        keys = [f"{self.key_prefix}{current_time - i}" for i in range(self.time_window)]
        print(keys)

        total_requests = sum(self.redis.llen(key) for key in keys)

        if total_requests >= self.max_requests:
            return False

        self.redis.rpush(key, 1)
        self.redis.expire(key, self.time_window)

        return True


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
