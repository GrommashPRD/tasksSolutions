class RedisQueue:
    def __init__(self):
        self.queue = []

    def publish(self, msg: dict):
        self.queue.append(msg)

    def consume(self) -> dict:
        return self.queue.pop(0) if self.queue else None

if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
