import redis


class RedisDao(object):
    """
    redis工具类
    """
    r = None
    redis_host = '127.0.0.1'
    redis_port = 6380

    def __init__(self):
        self.r = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)

    def get_redis(self):
        return self.r

    def set_value(self, key, value):
        self.r.set(key, value)

    def get_value(self, key):
        return self.r.get(key)


if __name__ == '__main__':
    redis = RedisDao()
    test_value = redis.get_value('test1')
    print(test_value)
    redis.set_value('test1', 'aaa')
    test_value = redis.get_value('test1')
    print(test_value)
